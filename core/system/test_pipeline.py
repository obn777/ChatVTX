# core/system/test_pipeline.py

from core.behavior.mode_manager import ModeManager


# --- MOCK COGNITIVE ---
def cognitive_process(user_input: str) -> str:
    return f"[COGNITIVE OUTPUT]\nAnalyzed: {user_input}"


# --- MOCK ENGINE ---
def engine_generate(prompt: str) -> str:
    return f"[MODEL RESPONSE]\n{prompt}"


def run_test():
    mode_manager = ModeManager()

    # Переключим режим для проверки
    mode_manager.set_mode("strategic")

    user_input = "Should we decentralize the system?"

    # 1. Cognitive layer
    cognitive_output = cognitive_process(user_input)

    # 2. Behavior modify prompt
    mode = mode_manager.get_mode()
    modified_prompt = mode.modify_prompt(cognitive_output)

    # 3. Engine
    model_output = engine_generate(modified_prompt)

    # 4. Postprocess
    final_output = mode.postprocess(model_output)

    print("=== FINAL OUTPUT ===")
    print(final_output)


if __name__ == "__main__":
    run_test()
