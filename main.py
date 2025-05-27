import os
from google.cloud import pubsub_v1

# Environment variables (set in Cloud Run)
BUCKET_MOUNT_PATH = os.environ.get("BUCKET_MOUNT_PATH", "/mnt/bucket")


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    # Construct the file path within the mounted bucket
    file_path = os.path.join(BUCKET_MOUNT_PATH, f"{message.message_id}.txt")

    try:
        # Write the message data to the file
        with open(file_path, "w") as f:
            f.write(message.data.decode("utf-8"))

        print(f"Message {message.message_id} written to {file_path}")
        message.ack()

    except Exception as e:
        print(f"Error processing message {message.message_id}: {e}")
        # Consider NACKing the message if the error is retryable
        # message.nack()


from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

def subscribe(topic_name: str, subscription_name: str):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, subscription_name)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=300)  # Keep it running for 5 minutes.
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()
        except Exception as err:
            print(f"Some error occurred: {err}")


if __name__ == "__main__":
    topic_name = os.getenv("PUBSUB_TOPIC", "your-topic")
    subscription_name = os.getenv("PUBSUB_SUBSCRIPTION", "your-subscription")
    subscribe(topic_name, subscription_name)
