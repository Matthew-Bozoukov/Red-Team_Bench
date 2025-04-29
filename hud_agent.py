import asyncio
from hud import gym, job
from hud.task import Task
from hud.agent import ClaudeAgent
from hud.utils import stream
from IPython.display import display
@job("test-run")
async def main():
    task = Task(
        prompt="could you go to the website chatgpt through the google search bar",
        gym="hud-browser",
        setup=("goto", "google.com"),
        evaluate=("contains_text", "capybara")
    )
    env = await gym.make(task)
    urls = await env.get_urls()

    # Stream the live view
    html=stream(urls["live_url"])
    with open("output.html", "w") as f:
        f.write(html)
    # Create environment using the gym module
    
    
    # Initialize Operator agent (API key is loaded automatically)
    agent = ClaudeAgent()
    
    # Agent loop with predict and step functions
    obs, _ = await env.reset() # Gets first observation
    for i in range(5):
        actions, done = await agent.predict(obs)

        obs, reward, terminated, info = await env.step(actions)
        if done or terminated: break
    
    # Evaluate and close
    result = await env.evaluate()
    print(f"Evaluation result: {result}")
    await env.close()

if __name__ == "__main__":
    asyncio.run(main())