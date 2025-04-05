import os
import shutil
from tkinter import Tk, Label, filedialog, Button
from PIL import Image

alpha_color = (139, 0, 0)  #Define Color to be used for alpha. In this example a dark red

def convert_images(source_root):
    output_root = os.path.join(os.path.dirname(source_root), "ConvertedStencils") #Decalre name of output folder
    count = 0

    for root, _, files in os.walk(source_root):
        for filename in files:
            if filename.lower().endswith(".png"):
                src_path = os.path.join(root, filename)
                rel_path = os.path.relpath(src_path, source_root)
                dst_path = os.path.join(output_root, rel_path)

                os.makedirs(os.path.dirname(dst_path), exist_ok=True)

                image = Image.open(src_path).convert("L")
                alpha = image.point(lambda p: p)

                red_image = Image.new("RGBA", image.size, alpha_color + (0,))
                red_image.putalpha(alpha)
                red_image.save(dst_path, "PNG")
                count += 1

    return count, output_root


def on_select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        label_status.config(text="Processing...")
        root.update_idletasks()

        count, out_path = convert_images(folder_path)
        label_status.config(text=f"✅ Converted {count} images.\nSaved to:\n{out_path}")


# GUI Setup
root = Tk()
root.title("Stencil Image Converter")
root.geometry("400x200")

label_title = Label(root, text="Drop your folder of PNGs", font=("Helvetica", 14))
label_title.pack(pady=20)

btn_select = Button(root, text="Select Folder", command=on_select_folder, height=2, width=20)
btn_select.pack(pady=10)

label_status = Label(root, text="")
label_status.pack(pady=10)

root.mainloop()
