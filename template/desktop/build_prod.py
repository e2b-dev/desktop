from dotenv import load_dotenv
from e2b_template import Template
from .template import template

load_dotenv()

Template.build(
    template,
    alias="desktop",
    cpu_count=1,
    memory_mb=1024,
    on_build_logs=lambda log_entry: print(log_entry),
)
