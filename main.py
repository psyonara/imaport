import typer
from imap_tools import MailBox


def main(
    source_server: str = typer.Option(None, prompt=True),
    source_user: str = typer.Option(None, prompt=True),
    source_password: str = typer.Option(None, prompt=True),
    source_folder: str = typer.Option("*", prompt=True),
    destination_server: str = typer.Option(None, prompt=True),
    destination_user: str = typer.Option(None, prompt=True),
    destination_password: str = typer.Option(None, prompt=True)
):
    source_box = MailBox(source_server).login(source_user, source_password)
    destination_box = MailBox(destination_server).login(destination_user, destination_password)

    if source_folder == "*":
        folders = source_box.folder.list()
    else:
        folders = [source_folder]

    for folder in folders:
        source_box.folder.set(folder)

        folder_status = source_box.folder.status(folder)
        msg_count = folder_status["MESSAGES"]

        if not destination_box.folder.exists(folder):
            print(f"Creating folder '{folder}' in destination account...")
            destination_box.folder.create(folder)

        print(f"Importing {msg_count} messages from {folder}...")
        with typer.progressbar(source_box.fetch(), length=msg_count) as progress:
            for msg in progress:
                destination_box.append(msg, folder)


if __name__ == "__main__":
    typer.run(main)
