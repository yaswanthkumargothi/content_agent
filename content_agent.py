from langchain.agents import initialize_agent, AgentType
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from search_tools import create_search_tools
from prompts import CONTENT_SYSTEM_PROMPT, CONTENT_HUMAN_PROMPT

class ContentGenerator:
    def __init__(self):
        self.llm = Ollama(
            model="deepseek-r1:7b",
            temperature=0.7
        )
        self.search_tools = create_search_tools()
        
        # Create tool descriptions for the prompt
        self.tool_descriptions = "\n".join([
            f"- {tool.name}: {tool.description}" 
            for tool in self.search_tools
        ])
        
        self.agent = initialize_agent(
            tools=self.search_tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3,
            early_stopping_method="generate"
        )
        
        self.content_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                template=CONTENT_SYSTEM_PROMPT,
                input_variables=["topic", "platform", "tone", "tools"]
            )
        )

    def generate_content(self, topic: str, platform: str = "Twitter", tone: str = "Professional"):
        try:
            # First, gather information using the search agent
            search_query = f"Latest information about: {topic}"
            search_result = self.agent.run(search_query)
            
            # Generate content using the gathered information
            content = self.content_chain.run(
                topic=topic,
                platform=platform,
                tone=tone,
                tools=self.tool_descriptions,
            )
            
            return content.strip()
        except Exception as e:
            print(f"Debug - Error details: {str(e)}")
            return f"Error generating content. Please try again with a different query."

if __name__ == "__main__":
    generator = ContentGenerator()
    content = generator.generate_content(
        topic="New development projects in Visakhapatnam",
        platform="website Blog",
        tone="Professional"
    )
    print(content)
