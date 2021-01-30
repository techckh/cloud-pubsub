from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import os


def main():
    project_id = os.getenv('PROJECT_ID', None)
    assert project_id, 'error project id'

    subscription_id = 'my-sub'

    timeout = 10.0

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received {message}.")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()


if __name__ == '__main__':
    # should do gcloud pubsub subscriptions create my-sub --topic my-topic first
    main()
