import os
import json
import logging
import re
import unicodedata
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama, HuggingFaceEndpoint, HuggingFacePipeline
from langchain_groq import ChatGroq
from langchain_google_vertexai import VertexAIModelGarden
from huggingface_hub import AsyncInferenceClient
from pydantic import BaseModel
from typing import List
from crewai_tools import ( 
    # CodeDocsSearchTool,
    # CSVSearchTool,
    # DirectorySearchTool,
    # DirectoryReadTool,
    # DOCXSearchTool,
    # FileReadTool,
    # GithubSearchTool,
    SerperDevTool,
    # TXTSearchTool,
    # JSONSearchTool,
    # MDXSearchTool,
    # PDFSearchTool,
    # PGSearchTool,
    # RagTool,
    # ScrapeElementFromWebsiteTool,
    ScrapeWebsiteTool,
    # SeleniumScrapingTool,
    WebsiteSearchTool,
    # XMLSearchTool,
    # YoutubeChannelSearchTool,
    # YoutubeVideoSearchTool,
	)

@CrewBase
class CrewCriadorEmenta():
	def __init__(self):
		# API keys
		self.openai_api_key = os.getenv('OPENAI_API_KEY')
		self.claudeai_api_key = os.getenv('CLAUDE_API_KEY')
		self.huggingface_api_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
		self.groq_api_key = os.getenv('GROQ_API_KEY')
		# Language models
		self.openai_gpt4_llm = ChatOpenAI(model_name='gpt-4-turbo-2024-04-09', api_key=self.openai_api_key)
		self.openai_gpt35_llm = ChatOpenAI(model_name='gpt-3.5-turbo-0125', api_key=self.openai_api_key)
		self.claude_opus_llm = ChatAnthropic(model_name='claude-3-opus-20240229', anthropic_api_key=self.claudeai_api_key)
		self.claude_sonnet_llm = ChatAnthropic(model_name='claude-3-sonnet-20240229', anthropic_api_key=self.claudeai_api_key)
		self.claude_haiku_llm = ChatAnthropic(model_name='claude-3-haiku-20240307', anthropic_api_key=self.claudeai_api_key)  
		self.llama3_70b_llm = ChatGroq(model_name='llama3-70b-8192', groq_api_key=self.groq_api_key)
		self.llama3_8b_llm = ChatGroq(model_name='llama3-8b-8192', groq_api_key=self.groq_api_key)
		# self.llama3_8b_262k = VertexAIModelGarden(project="Projetos com IA", endpoint_id="llama-3-8b-instruct-262k")
		# Config files
		self.agents_config = 'config/agents.yaml'
		self.tasks_config = 'config/tasks.yaml'
		self.verbose_agents = True
		self.verbose_tasks = True


	'''
	Set up the agents
	'''
	@agent
	def pesquisador(self) -> Agent:
		return Agent(
			config=self.agents_config['pesquisador'],
			llm=self.claude_haiku_llm,
			verbose=self.verbose_agents,
			tools=[
				SerperDevTool(
					description="Search for articles on SerperDev",
				),
				ScrapeWebsiteTool(
					description="Use the ScrapeWebsiteTool to scrape the web for information",
				),
			],
			allow_delegation=True,
		)

	@agent
	def analista(self) -> Agent:
		return Agent(
			config=self.agents_config['analista'],
			llm=self.claude_haiku_llm,
			verbose=self.verbose_agents,
			allow_delegation=True,
		)

	@agent
	def ementa(self) -> Agent:
		return Agent(
			config=self.agents_config['ementa'],
			llm=self.claude_haiku_llm,
			verbose=self.verbose_agents,
			allow_delegation=True,
		)

	# @agent
	def criador_aula(self) -> Agent:
		return Agent(
			config=self.agents_config['criador_aula'],
			llm=self.claude_haiku_llm,
			verbose=self.verbose_agents,
			allow_delegation=True,
		)
	


	'''
	Set up the tasks
	'''
	@task
	def _pesquisa(self) -> Task:
		return Task(
			config=self.tasks_config['_pesquisa'],
			agent=self.pesquisador(),
			verbose=self.verbose_tasks,
			output_file='./tasks_outputs/task1.md'
		)

	@task
	def _analise_1(self) -> Task:
		context=[self._pesquisa()]
		return Task(
			config=self.tasks_config['_analise_1'],
			agent=self.analista(),
			context=context,
			verbose=self.verbose_tasks,
			output_file='./tasks_outputs/task2_1.md'
		)

	@task
	def _analise_2(self) -> Task:
		context=[self._pesquisa()]
		return Task(
			config=self.tasks_config['_analise_2'],
			agent=self.analista(),
			context=context,
			verbose=self.verbose_tasks,
			output_file='./tasks_outputs/task2_2.md'
		)

	@task
	def _analise_3(self) -> Task:
		context=[self._pesquisa()]
		return Task(
			config=self.tasks_config['_analise_3'],
			agent=self.analista(),
			context=context,
			verbose=self.verbose_tasks,
			output_file='./tasks_outputs/task2_3.md'
		)

	@task
	def _analise_4(self) -> Task:
		context=[self._pesquisa()]
		return Task(
			config=self.tasks_config['_analise_4'],
			agent=self.analista(),
			context=context,
			verbose=self.verbose_tasks,
			output_file='./tasks_outputs/task2_4.md'
		)

	@task
	def _analise_5(self) -> Task:
		context=[self._pesquisa()]	
		return Task(
			config=self.tasks_config['_analise_5'],
			agent=self.analista(),
			context=context,
			verbose=self.verbose_tasks,
			output_file='./tasks_outputs/task2_5.md'
		)

	@task
	def _ementa(self) -> Task:
		context=[
			self._analise_1(),
			self._analise_2(),
			self._analise_3(),
			self._analise_4(),
			self._analise_5(),
		]
		return Task(
			config=self.tasks_config['_ementa'],
			agent=self.ementa(),
			context=context,
			verbose=self.verbose_tasks,
			output_file='./tasks_outputs/task3.md'
		)

	# @task
	def _criacao(self) -> Task:
		context=[
			self._ementa(),
		]
		return Task(
			config=self.tasks_config['_criacao'],
			agent=self.criador_aula(),
			context=context,
			verbose=self.verbose_tasks,
			output_file='./tasks_outputs/task4.md'
		)


	'''
	Set up the crew
	'''
	@crew
	def crew(self) -> Crew:
		"""Creates the CriadorAulas crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			full_output=True,
		)