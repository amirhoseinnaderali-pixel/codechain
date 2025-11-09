from google import genai
from typing import List, Dict
import json
import re
from datetime import datetime



# Initialize client
def get_client(api_key: str):
    return genai.Client(api_key=api_key)

# Define your 30+ models in sequential order
MODEL_CHAIN1 = [
    # Round 1: Elite reasoning
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    
    # Round 2: Thinking models
    "gemini-2.0-flash-thinking-exp",
    "gemini-2.5-flash",
    "gemini-2.0-flash-001",
    
    # Round 3: More flash models
    "gemini-2.5-flash-preview-05-20",
    "gemini-flash-latest",
    "gemini-2.0-flash-exp",
    
    # Round 4: Back to pro
    "gemini-pro-latest",
    "gemini-2.5-flash",
    "gemini-2.0-flash-lite",
    
    # Round 5: Lite models
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash-lite-preview-06-17",
    "gemini-flash-lite-latest",
    
    # Round 6: Thinking again
    "gemini-2.0-flash-thinking-exp-01-21",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    
    # Round 7: More variations
    "gemini-2.0-flash-thinking-exp-1219",
    "gemini-2.5-flash-preview-09-2025",
    "gemini-2.0-flash-lite",
    
    # Round 8: Gemma models
    "gemma-3-27b-it",
    "gemini-2.5-flash",
    "gemma-3-12b-it",
    
    # Round 9: Back to elite
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.0-flash-thinking-exp",
    
    # Round 10: Final polish
    "gemini-2.5-flash-lite-preview-09-2025",
    "gemini-2.0-flash",
    "gemini-2.5-pro",  # Final elite model
]
MODEL_CHAIN2 = [
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.0-flash-thinking-exp",
    "gemini-2.5-flash-lite-preview-09-2025",
    "gemini-2.0-flash",
    "gemini-2.5-pro",
]
MODEL_CHAIN3 = [
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.0-flash-thinking-exp",
    "gemini-2.5-pro"
]
OPTIMIZED_MODEL_CHAIN = [
    # === ROUND 1: Elite Opening (3 models) ===
    "gemini-2.5-pro",              # 1. Best model - set strong foundation
    "gemini-2.5-flash",            # 2. Fast refinement
    "gemini-2.0-flash-thinking-exp", # 3. Deep reasoning check
    
    # === ROUND 2: Controlled Chaos (3 models) ===
    "gemini-2.0-flash-lite",       # 4. Inject noise (weak model)
    "gemma-3-27b-it",              # 5. Different perspective (Gemma)
    "gemini-2.5-flash-lite",       # 6. More noise
    
    # === ROUND 3: Consolidation (3 models) ===
    "gemini-2.5-flash",            # 7. Merge ideas
    "gemini-2.0-flash-thinking-exp-01-21", # 8. Thinking + consolidation
    "gemini-2.5-pro",              # 9. Elite correction
    
    # === ROUND 4: Final Polish (3 models) ===
    "gemini-2.0-flash",            # 10. Fast final check
    "gemini-2.5-flash",            # 11. One more refinement
    "gemini-2.5-pro",              # 12. Final elite polish
]



AGGRESSIVE_CHAIN = [
    # === Opening: Elite + Thinking ===
    "gemini-2.5-pro",                    # 1. Strong start
    "gemini-2.0-flash-thinking-exp",     # 2. Deep reasoning
    
    # === Exploration: Inject Noise ===
    "gemini-2.0-flash-lite",             # 3. Weak model (noise)
    "gemma-3-27b-it",                    # 4. Different architecture
    
    # === Consolidation ===
    "gemini-2.5-flash",                  # 5. Fast merge
    "gemini-2.0-flash-thinking-exp-01-21", # 6. Thinking consolidation
    
    # === Final Polish ===
    "gemini-2.5-pro",                    # 7. Elite polish
    "gemini-2.5-flash",                  # 8. Last refinement
    "gemini-2.5-pro",                    # 9. Final FINAL check
]

BALANCED_CHAIN = [
    # === ROUND 1: Strong Foundation (4 models) ===
    "gemini-2.5-pro",                    # 1. Elite opening
    "gemini-2.5-flash",                  # 2. Quick refine
    "gemini-2.0-flash-thinking-exp",     # 3. Deep think
    "gemini-2.5-flash",                  # 4. Consolidate R1
    
    # === ROUND 2: Exploration (4 models) ===
    "gemini-2.0-flash-lite",             # 5. Noise
    "gemma-3-27b-it",                    # 6. Different view
    "gemini-2.5-flash-lite",             # 7. More noise
    "gemini-2.0-flash",                  # 8. Stabilize
    
    # === ROUND 3: Correction (4 models) ===
    "gemini-2.5-pro",                    # 9. Elite correction
    "gemini-2.0-flash-thinking-exp-01-21", # 10. Thinking check
    "gemini-2.5-flash",                  # 11. Merge
    "gemini-pro-latest",                 # 12. Another elite view
    
    # === ROUND 4: Final (3 models) ===
    "gemini-2.5-flash",                  # 13. Pre-polish
    "gemini-2.0-flash-thinking-exp-1219", # 14. Final thinking
    "gemini-2.5-pro",                    # 15. Ultimate polish
]


MODEL_CHAIN4 = [
    # Start with base models for initial processing
    "gemini-2.0-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash",
    
    # Build up with lite variants
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-lite",
    
    # Introduce smaller Gemma for diversity
    "gemma-3-12b-it",
    
    # Add experimental basics
    "gemini-2.0-flash-001",
    
    # Experimental expansions
    "gemini-2.0-flash-exp",
    
    # Thinking experiments progression
    "gemini-2.0-flash-thinking-exp",
    "gemini-2.0-flash-thinking-exp",
    "gemini-2.0-flash-thinking-exp-01-21",
    "gemini-2.0-flash-thinking-exp-1219",
    
    # Lite flash latest and variants
    "gemini-flash-lite-latest",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash-lite-preview-06-17",
    
    # Core flash models
    "gemini-flash-latest",
    "gemini-2.5-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash",
    
    # Flash previews for advanced features
    "gemini-2.5-flash-preview-05-20",
    "gemini-2.5-flash-lite-preview-09-2025",
    "gemini-2.5-flash-preview-09-2025",
    
    # Larger Gemma for heavy lifting
    "gemma-3-27b-it",
    
    # Latest pro for refinement
    "gemini-pro-latest",
    
    # Elite pro models for final strength
    "gemini-2.5-pro",
    "gemini-2.5-pro",
    "gemini-2.5-pro"  # Ultimate polish
,
"gemini-2.0-flash-001",
"gemini-2.5-pro",

]


















# Mode to Model Chain mapping
def get_model_chain_by_mode(mode: str = "fast") -> List[str]:
    """Get the appropriate model chain based on mode"""
    mode = mode.lower()
    if mode == "full power" or mode == "fullpower" or mode == "full":
        return MODEL_CHAIN1
    elif mode == "advance" or mode == "advanced":
        return MODEL_CHAIN2
    elif mode == "optimized":
        return OPTIMIZED_MODEL_CHAIN
    elif mode == "aggressive":
        return AGGRESSIVE_CHAIN
    elif mode == "balanced":
        return BALANCED_CHAIN
    elif mode == "strongest":
        return MODEL_CHAIN4
    else:  # default to fast
        return MODEL_CHAIN3








def call_model(model_name: str, prompt: str, api_key: str) -> Dict:
    """Call a single model and return result"""
    client = get_client(api_key)
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        
        return {
            "model": model_name,
            "output": response.text,
            "success": True,
            "error": None
        }
    except Exception as e:
        return {
            "model": model_name,
            "output": "",
            "success": False,
            "error": str(e)
        }

def sequential_model_chain(
    initial_task: str,
    api_key: str,
    models: List[str] = None,
    verbose: bool = True
) -> Dict:

    if models is None:
        models = MODEL_CHAIN3  # Default to fast mode
    
    if verbose:
        print("\n" + "="*80)
        print("🔗 SEQUENTIAL MODEL CHAIN - STARTING")
        print("="*80)
        print(f"📋 Initial Task: {initial_task[:100]}...")
        print(f"🤖 Total Models: {len(models)}")
        print("="*80 + "\n")
    
    results = []
    current_output = initial_task
    
    for i, model in enumerate(models, 1):
        if verbose:
            print(f"\n{'─'*80}")
            print(f"🤖 [{i}/{len(models)}] Processing with: {model}")
            print(f"{'─'*80}")
        
        # Create refinement prompt
        if i == 1:
            # First model gets the original task
            prompt = f"""You are the first model in a chain of {len(models)} AI models working together.

Task: {current_output}

Your job: Analyze this task and provide your best solution/analysis. The next model will refine your output.

Provide a detailed, complete response."""
        else:
            # Subsequent models refine previous output
            prompt = f"""You are model {i} in a chain of {len(models)} AI models working together.

Original Task: {initial_task}

Previous Model ({results[-1]['model']}) Output:
{current_output}

Your job: Review the previous output and IMPROVE it by:
1. Fixing any errors or issues
2. Adding missing details
3. Improving clarity and quality
4. Optimizing the solution
5. Making it more complete

Provide your improved version. The next model will further refine it."""
        
        # Call the model
        result = call_model(model, prompt, api_key)
        
        if result["success"]:
            current_output = result["output"]
            if verbose:
                print(f"✅ Success! Output length: {len(current_output)} chars")
                print(f"Preview: {current_output[:200]}...")
        else:
            if verbose:
                print(f"❌ Failed: {result['error']}")
                print(f"⚠️  Using previous output")
        
        results.append({
            **result,
            "step": i,
            "timestamp": datetime.now().isoformat()
        })
    
    if verbose:
        print("\n" + "="*80)
        print("✨ SEQUENTIAL CHAIN COMPLETED")
        print("="*80)
        print(f"✅ Successful calls: {sum(1 for r in results if r['success'])}/{len(results)}")
        print(f"📊 Final output length: {len(current_output)} chars")
        print("="*80 + "\n")
    
    return {
        "initial_task": initial_task,
        "final_output": current_output,
        "all_steps": results,
        "total_models": len(models),
        "successful_models": sum(1 for r in results if r["success"]),
        "completed_at": datetime.now().isoformat()
    }

def display_chain_results(result: Dict, show_all_steps: bool = False):
    """Display the results nicely"""
    print("\n" + "="*100)
    print("📋 INITIAL TASK")
    print("="*100)
    print(result["initial_task"])
    
    if show_all_steps:
        print("\n" + "="*100)
        print("🔗 ALL PROCESSING STEPS")
        print("="*100)
        for step in result["all_steps"]:
            print(f"\n{'─'*100}")
            print(f"Step {step['step']}: {step['model']}")
            print(f"Status: {'✅ Success' if step['success'] else '❌ Failed'}")
            if step["success"]:
                print(f"Output preview:\n{step['output'][:300]}...")
            else:
                print(f"Error: {step['error']}")
    
    print("\n" + "="*100)
    print("🎯 FINAL OUTPUT (after all models)")
    print("="*100)
    print(result["final_output"])
    
    print("\n" + "="*100)
    print("📊 STATISTICS")
    print("="*100)
    print(f"Total models in chain: {result['total_models']}")
    print(f"Successful calls: {result['successful_models']}")
    print(f"Success rate: {(result['successful_models']/result['total_models']*100):.1f}%")

def save_chain_results(result: Dict, filename: str = "chain_output"):
    """Save results to file"""
    import os
    
    os.makedirs(f"{filename}_results", exist_ok=True)
    
    # Save final output
    with open(f"{filename}_results/final_output.txt", "w") as f:
        f.write(result["final_output"])
    
    # Save all steps
    with open(f"{filename}_results/all_steps.json", "w") as f:
        json.dump(result, f, indent=2)
    
    # Save summary
    with open(f"{filename}_results/summary.txt", "w") as f:
        f.write(f"Initial Task: {result['initial_task']}\n\n")
        f.write(f"Total Models: {result['total_models']}\n")
        f.write(f"Successful: {result['successful_models']}\n")
        f.write(f"Completed: {result['completed_at']}\n\n")
        f.write("="*80 + "\n")
        f.write("FINAL OUTPUT:\n")
        f.write("="*80 + "\n")
        f.write(result["final_output"])
    
    print(f"\n💾 Results saved to: {filename}_results/")

# Example usage


def super_code_generator(task: str, api_key: str, mode: str = "fast") -> str:
    """Generate a super code for the task
    
    Args:
        task: The task description
        api_key: Google AI Studio API key
        mode: "fast", "advance", or "full power" - determines which model chain to use
    """
    # Get the appropriate model chain based on mode
    models = get_model_chain_by_mode(mode)
    
    #result = sequential_model_chain(
     #   initial_task=task,
      #  api_key=api_key,
       # models=models,
        #verbose=True
    #)
    result=sequential_model_chain_with_full_history(
        initial_task=task,
        api_key=api_key,
        models=models,
        verbose=True,
        scoring_enabled=True,
        select_best_from_all=False
    )

    return result["final_output"]





def sequential_model_chain_with_full_history(
    initial_task: str,
    api_key: str,
    models: List[str] = None,
    verbose: bool = True,
    scoring_enabled: bool = True,
    select_best_from_all: bool = False
) -> Dict:


    
    results = []
    current_output = initial_task
    all_responses = []  # Store all successful responses with scores
    all_outputs_history = []  # Store all outputs for history tracking
    best_selections = []  # Track when best selection occurs
    
    for i, model in enumerate(models, 1):

        # Create refinement prompt
        if i == 1:
            prompt = f"""You are the first model in a chain of {len(models)} AI models working together.

Task: {current_output}

Your job: Analyze this task and provide your best solution/analysis. The next model will refine your output.

Provide a detailed, complete response
HINT:
1. Task completion (30 points)
2. Code quality (25 points)
3. Documentation (20 points)
4. Error handling (15 points)
5. Completeness (10 points)
."""
        else:
            # For models after first, we can include history if select_best_from_all is True
            prompt = f"""You are model {i} in a chain of {len(models)} AI models working together.

            Original Task: {initial_task}

            Previous Model ({results[-1]['model']}) Output:
            {current_output}


            Your job: Review the previous output and IMPROVE it by:
            1. Fixing any errors or issues
            2. Adding missing details
            3. Improving clarity and quality
            4. Optimizing the solution
            5. Making it more complete

            Provide your improved version.
            HINT:
            1. Task completion (30 points)
            2. Code quality (25 points)
            3. Documentation (20 points)
            4. Error handling (15 points)
            5. Completeness (10 points)
            """   
    
        
        # Call the model
        result = call_model(model, prompt, api_key)
        
        if result["success"]:
            
            current_output = result["output"]
            
            
            # Evaluate and store with score
            if scoring_enabled:
                evaluation = evaluate_response_quality(current_output,initial_task,api_key)
                print(f"score is know model {model} {evaluation['score']}"+"step number is "+str(i))
                scored_response = {
                    "step": i,
                    "model": model,
                    "output": current_output,
                    "score": evaluation["score"]+i,
                    "success": True
                }
                all_responses.append(scored_response)
                
                current_output,score,model=find_best_response(all_responses)
                print(f"best  score: {score}"+"step number is "+str(i))
                print(f"best  output: {model}")
                
                


                
                
        
        results.append({
            **result,
            "step": i,
            "timestamp": datetime.now().isoformat()
        })
        
        # BEST SELECTION LOGIC - After each model (except first)


    
    return {
        "initial_task": initial_task,
        "final_output": current_output,
        "all_steps": results,
        "all_responses": all_responses,
        "all_outputs_history": all_outputs_history,
        "best_selections": best_selections,
        "total_models": len(models),
        "successful_models": sum(1 for r in results if r["success"]),
        "scoring_enabled": scoring_enabled,
        "select_best_from_all": select_best_from_all,
        "completed_at": datetime.now().isoformat()
    }




def evaluate_response_quality(response: str, original_task: str, api_key: str) -> Dict:
    """Evaluate the quality of a response against the original task."""
    try:
        evaluation_prompt = f"""
You are an AI response evaluator. Score this response on a scale of 1-100 based on:
1. Task completion (30 points): How well does it address the original task?
2. Code quality (25 points): Is the code clean, efficient, and well-structured?
3. Documentation (20 points): Is it well-documented and explained?
4. Error handling (15 points): Does it handle edge cases and errors?
5. Completeness (10 points): Is the solution complete and usable?

CRITICAL: You MUST respond with ONLY a single number between 1-100. No explanations, no text, just the number.

Example:
85

Original Task: {original_task}

Response to Evaluate:
{response}

Your score (number only):"""
        
        evaluation_result = call_model("gemini-2.5-flash", evaluation_prompt, api_key)
        
        # Debug: چاپ نتیجه کامل
        print(f"DEBUG - Full evaluation result: {evaluation_result}")
        
        if evaluation_result.get("success"):
            score_text = evaluation_result.get("output", "").strip()
            print(f"DEBUG - Score text: '{score_text}'")
            
            # روش‌های مختلف برای استخراج عدد
            # روش 1: اگر فقط عدد باشد
            if score_text.isdigit():
                score = int(score_text)
                #print(f"DEBUG - Method 1 (pure digit): {score}")
            else:
                # روش 2: پیدا کردن همه اعداد
                numbers = re.findall(r'\d+', score_text)
                #print(f"DEBUG - Found numbers: {numbers}")
                
                if numbers:
                    # اگر چند عدد هست، آخری را بگیر (معمولاً نمره نهایی است)
                    score = int(numbers[-1])
                    print(f"DEBUG - Method 2 (regex): {score}")
                else:
                    #print("DEBUG - No numbers found, using default 50")
                    score = 50
            
            # محدود کردن به بازه 1-100
            score = min(100, max(1, score))
            
            return {
                "score": score, 
                "success": True,
                "raw_output": score_text  # برای دیباگ
            }
        else:
            error_msg = evaluation_result.get("error", "Unknown error")
            print(f"DEBUG - Evaluation failed: {error_msg}")
            return {
                "score": 50, 
                "success": False, 
                "error": f"Evaluation failed: {error_msg}"
            }
    
    except Exception as e:
        print(f"DEBUG - Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "score": 50, 
            "success": False, 
            "error": f"Exception: {str(e)}"
        }


def find_best_response(all_responses):
    temp = -1
    best_response = None

    for r in all_responses:
        #print(f"response: {r['model']} {r['score']}")
        if r["score"] > temp:
            #print(f"best response: {r['model']} {r['score']}")
            temp = r["score"]
            best_response = r

        #print(f"current best: {best_response['model']} {best_response['score']}")

    return best_response["output"], temp, best_response["model"]




if __name__ == "__main__":
    print(super_code_generator("write a code to generate a random number", "AIzaSyAtVovqpNtYpy30EDTr9nxlkdHQxbntq4k", "fast"))  






