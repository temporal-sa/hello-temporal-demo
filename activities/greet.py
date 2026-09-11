from temporalio import activity


@activity.defn
def greet(name: str) -> str:
    return f"Hello, {name}!"
