import streamlit as st

swara = {1: "S", 2: "R", 3: "G", 4: "M", 5: "P", 6: "D", 7: "N",
         8: "Ṡ", 9: "Ṙ", 10: "Ġ", 11: "Ṁ", 12: "Ṗ"}

def convert_to_numbers(input_text):
    ls = input_text.split()
    output_text = ""
    doub_ct = 0
    for i in ls:
        if i == "│" or i == "|":
            output_text += "| "
            continue
        elif i == "‖" or i == "||":
            output_text += "‖ "
            doub_ct += 1
            if doub_ct % 2 == 0:
                output_text += "\n"
                st.write(output_text)
                output_text = ""
            continue
        elif i in swara.values():
            a = list(swara.keys())[list(swara.values()).index(i)]
            output_text += f"{a} "
        else:
            output_text += f"{i} "
    

def main():
    st.title("Swara to Number Converter App")

    input_text = st.text_input("Enter text:")
    if st.button("Convert"):
        convert_to_numbers(input_text)
        #st.write(output_text)

"""if __name__ == "__main__":
    main()"""
