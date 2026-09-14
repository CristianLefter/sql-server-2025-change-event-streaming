import os

from azure.eventhub import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblob import BlobCheckpointStore


CONSUMER_GROUP = "ces-demo-consumer"
CHECKPOINT_CONTAINER = "ces-demo-checkpoints"


def on_event(partition_context, event):
    if event is None:
        return

    print("\n=== CES EVENT RECEIVED ===")
    print(f"Partition: {partition_context.partition_id}")
    print(f"Sequence:  {event.sequence_number}")
    print(f"Offset:    {event.offset}")
    print()
    print(event.body_as_str(encoding="UTF-8"))
    print("==========================")

    partition_context.update_checkpoint(event)


def main():
    checkpoint_store = BlobCheckpointStore.from_connection_string(
        os.environ["CHECKPOINT_STORAGE_CONNECTION_STRING"],
        CHECKPOINT_CONTAINER,
    )

    client = EventHubConsumerClient.from_connection_string(
        os.environ["EVENTHUB_CONNECTION_STRING"],
        consumer_group=CONSUMER_GROUP,
        checkpoint_store=checkpoint_store,
    )

    print("Waiting for new CES events... Press Ctrl+C to stop.")

    try:
        with client:
            client.receive(
                on_event=on_event,
                starting_position="@latest",
            )
    except KeyboardInterrupt:
        print("\nConsumer stopped.")


if __name__ == "__main__":
    main()
