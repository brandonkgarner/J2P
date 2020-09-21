import json
from json import JSONDecodeError
import tkinter as tk


def json_to_py(my_str):
    return json.loads(my_str)


def py_to_json(my_dict):
    my_dict = my_dict.replace('\'', '\"')
    my_dict = my_dict.replace('T', 't')
    my_dict = my_dict.replace('F', 'f')

    return json.loads(json.dumps(my_dict))


def callback_json(sv):
    if master.focus_get()._name == '!entry':
        current_text = sv.get()
        if current_text:
            if current_text[0] == '0':
                pass
            else:
                try:
                    returned_text = json_to_py(current_text)
                    e2.delete(0, 'end')
                    e2.insert(0, returned_text)
                    l1.config(fg='black')
                # JSON builtin validation
                except JSONDecodeError:
                    mark_invalid(l1, e2)


def callback_py(sv):
    if master.focus_get()._name == '!entry2':
        current_text = sv.get()
        if current_text:
            if current_text[0] == '0':
                pass
            else:
                # Some basic validation
                if current_text[0] != '{' \
                        or current_text[-1] != '}' \
                        or (len(current_text.replace(' ', '')) >= 3 and current_text.replace(' ', '')[-2] == ','):
                    mark_invalid(l2, e1)
                else:
                    try:
                        eval(current_text)
                        returned_text = py_to_json(current_text)
                        e1.delete(0, 'end')
                        e1.insert(0, returned_text)
                        l2.config(fg='black')
                    except SyntaxError:
                        mark_invalid(l2, e1)


def mark_invalid(label_to_red, field_to_clear):
    label_to_red.config(fg='red')
    field_to_clear.delete(0, 'end')


def copy_json():
    master.clipboard_clear()
    master.clipboard_append(e1.get())


def copy_py():
    master.clipboard_clear()
    master.clipboard_append(e2.get())


def clear_fields():
    e1.delete(0, 'end')
    e2.delete(0, 'end')
    l1.config(fg='black')
    l2.config(fg='black')


# Right-click menu
# https://gist.github.com/angeloped/91fb1bb00f1d9e0cd7a55307a801995f

def make_textmenu(root):
    global the_menu
    the_menu = tk.Menu(root, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")
    the_menu.add_separator()
    the_menu.add_command(label="Select all")


def callback_select_all(event):
    # select text after 50ms
    master.after(50, lambda: event.widget.select_range(0, 'end'))


def show_textmenu(event):
    e_widget = event.widget
    the_menu.entryconfigure("Cut", command=lambda: e_widget.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy", command=lambda: e_widget.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste", command=lambda: e_widget.event_generate("<<Paste>>"))
    the_menu.entryconfigure("Select all", command=lambda: e_widget.select_range(0, 'end'))
    the_menu.tk.call("tk_popup", the_menu, event.x_root, event.y_root)


# ----------


master = tk.Tk()

master.title("JSON <--> PyDict")
l1 = tk.Label(master, text="JSON")
l1.grid(row=0, padx=(15, 2))
l2 = tk.Label(master, text="PyDict")
l2.grid(row=1, padx=(15, 2))

sv = tk.StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: callback_json(sv))

sv2 = tk.StringVar()
sv2.trace("w", lambda name, index, mode, sv=sv: callback_py(sv2))

make_textmenu(master)

e1 = tk.Entry(master, width=100, textvariable=sv)
e2 = tk.Entry(master, width=100, textvariable=sv2)

# bind the right-click menu feature to all Entry widget
master.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_textmenu)
master.bind_class("Entry", "<Control-a>", callback_select_all)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

tk.Button(master, text='Copy', command=copy_json, padx=4).grid(row=0, column=2, sticky=tk.W, pady=4, padx=(2, 26))
tk.Button(master, text='Copy', command=copy_py, padx=4).grid(row=1, column=2, sticky=tk.W, pady=4, padx=(2, 26))
tk.Button(master, text='Clear', width=60, bd=4, command=clear_fields).grid(row=3, column=1, pady=5, padx=15)
# tk.Button(master,  text='Close', width=60, bd=4, command=master.quit).grid(row=3, column=1, pady=5, padx=15)

master.mainloop()
