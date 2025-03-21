import os
from dotenv import load_dotenv

from camel.memories import (
    ChatHistoryBlock,
    LongtermAgentMemory,
    MemoryRecord,
    ScoreBasedContextCreator,
    VectorDBBlock,
)
from camel.messages import BaseMessage
from camel.types import ModelType, OpenAIBackendRole
from camel.utils import OpenAITokenCounter
from camel.embeddings import OpenAIEmbedding
from camel.storages import TiDBStorage
from camel.agents import ChatAgent

load_dotenv()

# Initialize the memory
embedding =  OpenAIEmbedding()
memory = LongtermAgentMemory(
    context_creator=ScoreBasedContextCreator(
        token_counter=OpenAITokenCounter(ModelType.GPT_4O_MINI),
        token_limit=1024,
    ),
    vector_db_block=VectorDBBlock(
        storage=TiDBStorage(
            url_and_api_key=os.environ["DATABASE_URL"],
            vector_dim=embedding.get_output_dim(),
            collection_name="my_agent"
        )
    ),
)
memory._current_topic = "You are a curious agent wondering about the universe."

def chat_with_memories(user_message: str) -> str:
    # Retrieve relevant memories
    context, token_count = memory.get_context()
    memories_str = "\n".join(f"- {message['role']}: {message['content']}" for message in context)

    # Define Assistant system prompt.
    sys_msg = BaseMessage.make_assistant_message(
        role_name='Agent',
        content=f'You are a curious agent wondering about the universe.\n{memories_str}',
    )

    # Define a user message
    usr_msg = BaseMessage.make_user_message(
        role_name='User',
        content=user_message,
    )
    memory.write_record(MemoryRecord(
        message=usr_msg,
        role_at_backend=OpenAIBackendRole.USER,
    ))

    # Call the agent.
    agent = ChatAgent(system_message=sys_msg, memory=memory)
    response = agent.step(usr_msg)

    # Store the response in memory.
    res_msg = BaseMessage.make_assistant_message(
        role_name='Agent',
        content=response.msgs[0].content,
    )
    memory.write_record(MemoryRecord(
        message=res_msg,
        role_at_backend=OpenAIBackendRole.ASSISTANT,
    ))

    return res_msg.content

def main():
    print("Chat with AI (type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        print(f"AI: {chat_with_memories(user_input)}")

if __name__ == "__main__":
    main()