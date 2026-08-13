chat endpoint problem (idempotency problem and connection fail problem)

connection fail is safe as long as the frontend load the loadchat endpoint but I still implemented a solution for best practices


{
message = what is this ?
public_id = 233
cookie = 123ab
db
}

{
message = what is this ?
public_id = 233
cookie = 123ab
db
}

--------------------------------------------------------------
if chat_session is None:
        raise HTTPException(status_code=404, detail="No chat session found")
-------------------------------------------------------------- PASSED: because it just checks if there is a session in the database


try:
        message_history = get_messages(chat_session.id, public_id, db)

        llm_messages = [
            {"role": message.role, "content": message.content}
            for message in message_history
        ]

        user_message = Message(
            chat_session_id=chat_session.id, role="User", content=chat.message
        )
        db.add(user_message)

        generated_prompt = generate_memory_prompt(
            chat_session.product, llm_messages, chat.message
        )

        response = await chat_generate(generated_prompt)

        llm_message = Message(
            chat_session_id=chat_session.id, role="Assistant", content=response
        )
        db.add(llm_message)

        db.commit()

        return response

    except Exception:
        db.rollback()
        raise

---------------------------------------------------------------------
1st problem, user might get disconnected while chatting with the bot and the frontend might display that the bot did not respond so the user can just refresh the page, but if the frontend has autoload, I added a prevention for that scenario


2nd problem, if the 2 mirrored request both came here, the llm response will respond twice, the buyer should only get 1 response at a time but I can't really add a transaction here cause there's no need to since it will not error anyways, the it will just display both answer and it will get stored as well, so transaction is not a thing here, what should I add ? and what to do in this situation ?

I have here a problem which is duplicate request, we only want 1 message per time and not two and this is called an idempotency problem but not exactly as that 

Idempotency = You can perform the same operation multiple times, but the final result is the same as if you performed it once. 

but what we need is to lock the chat_session so that the user cannot send another request until the chat_session is unlocked.

I can do asyncio.Lock but there's a problem here, worker 1 might lock the chat session but worker 2 cannot see it so it will just proceed with the process as well, what we need is REDIS

why redis ? because redis gives all worker the same lock which is what we want

SCENARIO
user's interned dies after commit, now the user thinks it failed and did a refresh, now the frontend sends the same request again, without idempotency, the function is vulnerable from sending another request on the llm but with idempotency, it will check the idempotency key so and if it exist, then we send the previous llm's response to the user.


SOLUTION:

1.
We need the frontend to send idempotency_key to the backend because so that if the user retries, the idempotency_key is still the same. Why not backend ? Because backend doesn't know if the user retried, it just accepts request

2.
create an idempotency key table


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    id = mapped_column(UUID, primary_key=True, default=uuid4)
    key = mapped_column(String, unique=True, nullable=False)
    chat_session_id = mapped_column(
        UUID,
        ForeignKey("chat_sessions.id"),
        nullable=False,
    )
    response = mapped_column(Text, nullable=True)
    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


user chats => check the idempotency key on the db => if it exist, return the response, if not, pass to the llm

now if the user disconnects and the user refresh the page, then the function will return the last respons eof the llm

I mean I do have a load chat which loads the chat through query and it's completely fine if I didn't add this but why not ? I make application robust enough


Now for the redis lock, I just created a redis client and modified it so that I could lock a function call, how does it work ? 
So it locks the function for 30 seconds and and the other request needs to wait for 5 seconds before it could go pass, so what will happen is the QAQA is still preserved and it cannot be QQAA

what if the the function call is only 5 seconds ? we have a finally block the release the lock, the 30 seconds is just if something happened to the api and it doesn't process it, then after 30 seconds it will get released because if not, then it will be locked forever lol




