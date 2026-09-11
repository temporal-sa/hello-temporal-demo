import asyncio
import concurrent.futures
import os

from dotenv import load_dotenv
from temporalio.client import Client
from temporalio.envconfig import ClientConfig
from temporalio.worker import Worker

from activities.greet import greet
from workflows.greeting import GreetingWorkflow


async def main():
    load_dotenv()
    connect_config = ClientConfig.load_client_connect_config()
    client = await Client.connect(**connect_config)
    print(
        f"✅ Client connected to {client.service_client.config.target_host} "
        f"in namespace '{client.namespace}'"
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client,
            task_queue=os.getenv("TEMPORAL_TASK_QUEUE", "greeting"),
            workflows=[GreetingWorkflow],
            activities=[greet],
            activity_executor=activity_executor,
        )
        print("Python greeting worker starting...")
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
