import os
import glob
from tkinter import Tk, simpledialog, messagebox
from tkinter.filedialog import askdirectory

def select_folder(root):
    """ Tkinterのルートウィンドウを使ってユーザーにフォルダを選択させる。 """
    folder_selected = askdirectory(parent=root)  # ダイアログを表示して選択されたフォルダのパスを取得
    return folder_selected

def get_user_input(root, prompt):
    """ Tkinterのルートウィンドウとプロンプトメッセージを使ってユーザーからの入力を受け取る。 """
    input_value = simpledialog.askstring("Input", prompt, parent=root)  # 入力ダイアログを表示
    return input_value.strip() if input_value is not None else None  # 入力があればトリムして返し、なければNoneを返す

def find_files(folder, extension):
    """ 指定されたフォルダ内で、特定の拡張子を持つファイルを検索する。 """
    extension = extension.lstrip('.')  # 拡張子の前のドットを削除
    search_pattern = f'*.{extension}'  # 検索パターンを作成
    return glob.glob(os.path.join(folder, search_pattern))  # パターンに一致するファイルのリストを返す

def write_filenames_to_txt(files, output_file):
    """ ファイルリストをテキストファイルに書き込む。 """
    with open(output_file, 'w') as file:  # ファイルを開いて書き込み
        for filename in files:
            # ファイルの基本名を取得して書き込み
            file.write(f"{os.path.splitext(os.path.basename(filename))[0]}\n")

def main():
    root = Tk()
    root.withdraw()  # GUIのルートウィンドウを非表示に設定

    try:
        folder = select_folder(root)  # フォルダ選択を行う
        if not folder:
            messagebox.showerror("Error", "フォルダが選択されていません。終了します。")
            return

        extension = get_user_input(root, "ファイル拡張子を入力してください（ドットなし、例：txt）:")
        if not extension:
            messagebox.showerror("Error", "拡張子が提供されていません。終了します。")
            return

        output_directory = os.path.join(os.getcwd(), "filelister_output")  # 出力ディレクトリのパスを設定
        os.makedirs(output_directory, exist_ok=True)  # 出力ディレクトリがなければ作成

        output_filename = get_user_input(root, "出力ファイル名を入力してください:")
        if not output_filename:
            messagebox.showerror("Error", "出力ファイル名が提供されていません。終了します。")
            return
        if not output_filename.endswith('.txt'):
            output_filename += '.txt'  # ファイル名が.txtで終わらない場合は追加

        files = find_files(folder, extension)  # ファイル検索を行う
        if not files:
            messagebox.showinfo("Information", "指定された拡張子のファイルは見つかりませんでした。")
            return

        output_path = os.path.join(output_directory, output_filename)  # 出力ファイルの完全なパスを作成
        # ファイルが既に存在する場合は上書き確認
        if os.path.exists(output_path):
            if not messagebox.askyesno("Confirm", "ファイルは既に存在します。上書きしますか？"):
                return  # ユーザーが上書きを拒否した場合は処理を終了

        write_filenames_to_txt(files, output_path)  # ファイル名を出力ファイルに書き込む
        messagebox.showinfo("Success", f"ファイル名が {output_path} に書き込まれました")
    except Exception as e:
        messagebox.showerror("Error", f"エラーが発生しました: {e}")
    finally:
        root.destroy()  # プログラム終了時にTkinterウィンドウを破棄

if __name__ == '__main__':
    main()
