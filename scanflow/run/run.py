# -*- coding: utf-8 -*-
# Author: Gusseppe Bravo <gbravor@uni.pe>
# License: BSD 3 clause

import logging
import subprocess
import os
import docker
from multiprocessing import Pool
import time
import requests
import json
from scanflow import tools

from textwrap import dedent

logging.basicConfig(format='%(asctime)s -  %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

client = docker.from_env()


class Run:
    def __init__(self, workflower, verbose=True):
        """
        Example:
            deployer = Run(platform)

        Parameters:
            environment (object): The platform that comes from setup class.
            api_image_name (object): The platform that comes from setup class.
            predictor_port (object): The platform that comes from setup class.

        """
        # if environment is not None:
        #     self.platform = environment
        #     self.env_container = environment.env_container
        #     self.app_type = environment.app_type
        #     self.workflow = environment.workflow
        #     self.single_app_dir = environment.single_app_dir

        self.ad_paths = tools.get_scanflow_paths(workflower.app_dir)
        self.workflower = workflower
        self.workflows_user = workflower.workflows_user
        self.app_dir = workflower.app_dir
        self.verbose = verbose
        tools.check_verbosity(verbose)

        self.logs_workflow = None
        self.logs_build_image = None
        self.logs_run_ctn = None
        self.api_image_name = None
        self.api_container_name = None
        self.api_container_object = None
        self.workflows = list()
        # self.predictor_port = predictor_port

    def pipeline(self):
        self.run_workflow()
        # self.deploy()

        return self

    def run_workflows(self):
        """
        Build a environment with Docker images.

        Parameters:
            mlproject_name (str): Prefix of a Docker image.
        Returns:
            image (object): Docker image.
        """

        for wf_user in self.workflows_user:
            logging.info(f"[++] Running workflow: [{wf_user['name']}].")
            if 'parallel' in wf_user.keys():
                environments = self.run_workflow(wf_user, wf_user['parallel'])
            else:
                environments = self.run_workflow(wf_user)

            logging.info(f"[+] Workflow: [{wf_user['name']}] was run successfully.")
            workflow = {'name': wf_user['name'], 'envs': environments}
            self.workflows.append(workflow)

    def run_workflow(self, workflow, parallel=False):
        """
        Run a workflow that consists of several python files.

        Parameters:
            workflow (dict): Workflow of executions
            parallel (bool): Parallel execution
        Returns:
            image (object): Docker image.
        """
        # logging.info(f'Running workflow: type={self.app_type} .')
        # logging.info(f'[+] Running workflow on [{env_container_name}].')
        containers = []

        if parallel:
            steps = [step for step in workflow['executors']]
            pool = Pool(processes=len(steps))
            pool.map(tools.run_step, steps)
        else:
            for step in workflow['executors']:
                logging.info(f"[+] Running env: [{workflow['name']}:{step['name']}].")

                env_container, result = tools.run_step(step)
                containers.append({'name': step['name'],
                                   'ctn': env_container,
                                   'result': result.output.decode('utf-8')[:10]})

        return containers

    # def run_step(self, step):
    #     """
    #     Run a workflow that consists of several python files.
    #
    #     Parameters:
    #         workflow (dict): Workflow of executions
    #     Returns:
    #         image (object): Docker image.
    #     """
    #     # logging.info(f'Running workflow: type={self.app_type} .')
    #     # logging.info(f'[+] Running workflow on [{env_container_name}].')
    #     try:
    #         env_name = step['name']
    #         env_container = client.containers.get(env_name)
    #         if 'parameters' in step.keys():
    #             cmd = f"python {step['file']} {tools.format_parameters(step['parameters'])}"
    #             result = env_container.exec_run(cmd=cmd,
    #                                             workdir='/app/workflow')
    #         else:
    #             result = env_container.exec_run(cmd=f"python {step['file']}",
    #                                             workdir='/app/workflow')
    #
    #         # result = env_container.exec_run(cmd=f"python workflow/{self.workflow['main']}")
    #         logging.info(f"[+] Running ({step['file']}). ")
    #         logging.info(f"[+] Output:  {result.output.decode('utf-8')} ")
    #
    #         logging.info(f"[+] Environment ({env_name}) finished successfully. ")
    #
    #         return env_container, result
    #         # self.logs_workflow = result.output.decode("utf-8")
    #
    #     except docker.api.client.DockerException as e:
    #         logging.error(f"{e}")
    #         logging.error(f"[-] Environment [{step['name']}] has not started yet.")
    #
    #     return None


    def __repr__(self):
        workflows_names = [d['name'] for d in self.workflows]
        _repr = dedent(f"""
        Setup = (
            Workflows: {workflows_names}
        )
        """)
        return _repr

    # def __repr__(self):
    #     _repr = dedent(f"""
    #     Environment = (
    #         image: {self.env_image_name},
    #         container: {self.env_container_name},
    #         type={self.app_type}),
    #         tracker=0.0.0.0:{self.tracker_port}),
    #     """)
    #     return _repr


    def save_env(self, registry_name):
        """
        Run an image that yields a environment.

        Parameters:
            registry_name (str): Name of registry to save.

        Returns:
            containers (object): Docker container.
        """
        if self.app_type == 'single':
            try:
                # for name_ctn, ctn in self.env_container.items():
                self.api_container_object['ctn'].commit(repository=registry_name,
                                                        tag=self.api_container_object['image'],
                                                        message='First commit')
                logging.info(f"[+] Environment [{self.api_container_object['image']}] was saved to registry [{registry_name}].")

            except docker.api.client.DockerException as e:
                logging.error(f"{e}")
                logging.error(f"Container creation failed.")

