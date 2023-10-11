import subprocess

db_host = "db"
db_port = "5432"
db_name = "foo"
db_user = "postgres"
db_password = "postgres"

dump_file = "dump_file.sql"

pg_dump_command = [
    "pg_dump",
    f"--host={db_host}",
    f"--port={db_port}",
    f"--username={db_user}",
    f"--dbname={db_name}",
    f"--file={dump_file}",
]


def run_dump():
    try:
        subprocess.run(pg_dump_command, check=True)
        print(f"Database dumped to {dump_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error dumping the database: {e}")
