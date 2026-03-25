from utils import load_and_prepare_data, execute_chart_code, extract_code
from generate_chart_code import generate_code
from reflect_and_generate import reflect_on_image_and_regenerate

def run_workflow(
    instruction,
    out_path_v1,
    out_path_v2,
    generation_model,
    image_reflection_model
):
    df = load_and_prepare_data('coffee_sales.csv')

    # print(df.head(5))

    try:
        print("Generating chart code...")
        response = generate_code(instruction, out_path_v1, model=generation_model)
        code = extract_code(response)
        error = execute_chart_code(code, df)
        if error:
            print("Error while generating chart code: ", error)
        else:
            print("Chart generated successfully")

        print("Reflecting on the chart...")
        response = reflect_on_image_and_regenerate(
            instruction=instruction, 
            chart_path= None if error else out_path_v1, 
            out_path_v2 = out_path_v2, 
            code_v1=code,
            error=error,
            model=image_reflection_model
        )
        code_v2 = extract_code(response)
        data = json.loads(response)
        feedback = data["feedback"]
        print("Feedback: ", feedback)
        execute_chart_code(code=code_v2, df=df)
        print("Chart regenerated successfully")
    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":

    instruction="Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv."
    out_path_v1="chart_v1.png"
    out_path_v2="chart_v2.png"
    generation_model = "nvidia/nemotron-3-super-120b-a12b:free"
    image_reflection_model = "nvidia/nemotron-nano-12b-v2-vl:free"

    run_workflow(instruction, out_path_v1, out_path_v2, generation_model, image_reflection_model)


