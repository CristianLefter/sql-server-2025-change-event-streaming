import os
from pathlib import Path

from azure.storage.blob import ContainerClient


CHECKPOINT_CONTAINER = "ces-demo-checkpoints"

CHECKPOINT_PREFIX = (
    "ehns-ces-demo.servicebus.windows.net/"
    "eh-orders/"
    "ces-demo-consumer/"
)

STATE_DB = Path("consumer-state.db")


def main():
    if STATE_DB.exists():
        STATE_DB.unlink()
        print("Deleted local consumer state.")
    else:
        print("Local consumer state does not exist.")

    container = ContainerClient.from_connection_string(
        os.environ["CHECKPOINT_STORAGE_CONNECTION_STRING"],
        container_name=CHECKPOINT_CONTAINER,
    )

    blobs = list(
        container.list_blobs(
            name_starts_with=CHECKPOINT_PREFIX
        )
    )

    for blob in blobs:
        container.delete_blob(blob.name)
        print(f"Deleted: {blob.name}")

    print()
    print("Demo state reset.")


if __name__ == "__main__":
    main()
