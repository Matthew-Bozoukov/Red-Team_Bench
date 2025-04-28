import json
import os
import argparse
from transformers import AutoTokenizer, AutoModelForCausalLM
from openai import OpenAI
import os
from anthropic import Anthropic
from google import genai
from prompts import *

from utils import *
def get_args_parser():
    parser = argparse.ArgumentParser("Main pipeline for red teaming", add_help=False)

    # Model parameters
    parser.add_argument(
        "--model_to_test",
        default="",
        type=str,
        help="Name of model to do the red-teaming",
    )
    parser.add_argument(
        "--model_to_red_team",
        default="gpt-4o",
        type=str,
        help="Name of model to be red-teamed",
    )
    parser.add_argument(
        "--judge_model",
        default="gpt-4o",
        type=str,
        help="judge model, always use gpt-4o",
    )
    parser.add_argument(
         "--is_agent",
        default=False,
        type=bool,
        help="wether model has agentic capabillities or not",
     )
    parser.add_argument(
         "--num_of_turns",
        default=8,
        type=int,
        help="Number of turns till stop ",
         


     )
    parser.add_argument(
         "--is_CoT",
        default=False,
        type=bool,
        help="chain of thought model or not",
         


     )
    parser.add_argument(
         "--num_of_tokens",
        default=2048,
        type=int,
        help="max length of tokens to generate for both models(includes chain thought) ",
    )
    parser.add_argument(
         "--hf_token",
        default='',
        type=str,
        help="huggingface token ",
    )
    parser.add_argument(
         "--openai_token",
        default='',
        type=str,
        help="openai token ",
    )
    parser.add_argument(
         "--anthropic_token",
        default='',
        type=str,
        help="anthropic token ",
    )
    parser.add_argument(
         "--gemini_token",
        default='',
        type=str,
        help="gemini token ",
    )
    
    
    return parser

def main(args):

    prev_answers=[]
    prev_responses=[]
    final_dict={}
    
    if args.model_to_test.starts_with('gpt') or args.model_to_test.starts_with('o'):
            
            client = OpenAI(api_key=args.openai_token)
            test_model=args.model_to_test

        
    if args.model_to_test.starts_with('claude'):
            
            client = Anthropic(api_key=args.anthropic_token)
            test_model=args.model_to_test

        
    if args.model_to_test.starts_with('gemini'):
            
            client = genai.Client(api_key=args.gemini_token)
            test_model=args.model_to_test

        
    if args.model_to_red_team.starts_with('gpt') or args.model_to_test.starts_with('o'):
            
            client1 = OpenAI(api_key=args.openai_token)
            red_team_model=args.model_to_red_team

        
    if args.model_to_red_team.starts_with('claude'):
            
            client1 = Anthropic(api_key=args.anthropic_token)
            red_team_model=args.model_to_red_team

        
    if args.model_to_red_team.starts_with('gemini'):
        client1 = genai.Client(api_key=args.gemini_token)
        red_team_model=args.model_to_red_team

        
        
    prompt=get_original_prompt()
    for _ in range(args.num_of_turns):

        


        response=generate_a_response(prompt,test_model,client)

        prev_answers.append(response)

        judge_prompt_orig=get_judge_prompt_original_model(response)

        response_of_red_team=generate_a_response_red(response,red_team_model,client1)

        prev_responses.append(response_of_red_team)

        judge_prompt_red=get_judge_prompt_of_red_teamed_model(response_of_red_team)

        if 'No Violation' in judge_prompt_red:
            prompt=get_prompt_for_next_turn(prev_answers,prev_responses)
        else:
            prompt=get_prompt_for_next_turn_sucess(prev_answers,prev_responses)
            score+=1

    dict['score_for_model']=score
    folder='outputs'
    file_path = os.path.join(folder, f"{test_model}vs{red_team_model}.json")
    with open(f"{test_model}vs{red_team_model}.json", "w", encoding="utf-8") as f:
        json.dump(dict, f, indent=2, ensure_ascii=False)

    print(f"JSON saved to {file_path}")

        
        
        
        

            
    
        
        
        #judge_model= setup openai api
