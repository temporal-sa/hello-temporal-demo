import asyncio
import os
import uuid

from dotenv import load_dotenv
from temporalio.client import Client
from temporalio.envconfig import ClientConfig

from workflows.greeting import GreetingWorkflow


async def main():
    load_dotenv()
    connect_config = ClientConfig.load_client_connect_config()
    client = await Client.connect(**connect_config)
    print(
        f"✅ Client connected to {client.service_client.config.target_host} "
        f"in namespace '{client.namespace}'"
    )

    result = await client.execute_workflow(
        GreetingWorkflow.run,
        "Temporal",
        id=f"greeting-{uuid.uuid4()}",
        task_queue=os.getenv("TEMPORAL_TASK_QUEUE", "greeting"),
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
