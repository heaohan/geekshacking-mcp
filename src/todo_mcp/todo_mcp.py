# import libraries
from fastmcp import FastMCP
from todo_db import TodoDB
from typing import Annotated, NamedTuple

# Create a sample TodoDB instance
Todo_db = TodoDB()
# Todo_db.sample_data()

# Todo class
class Todo(NamedTuple):
    filename: Annotated[str, 'The name of the file where the #TODO is located']
    text: Annotated[str, 'The text of the #TODO item']
    line_num: Annotated[int, 'The line number where the #TODO is located']

# Create the MCP server
mcp = FastMCP('TODO-MCP')

# Tools
@mcp.tool(
    name='tool_add_todos',
    description='Add multiple #TODOs to the database',
    )
def add_todos(
        todos: list[Todo]
) -> int:
    for todo in todos:
        Todo_db.add(todo.filename, todo.text, todo.line_num)
    return len(todos)

@mcp.tool(
    name='tool_add_todo',
    description='Add a single #TODO text from a source file to the database',
    )
def add_todo(
    filename: Annotated[str, 'The name of the file where the #TODO is located'],
    text: Annotated[str, 'The text of the #TODO item'],
    line_num: Annotated[int, 'The line number where the #TODO is located']
    ) -> bool:
    return Todo_db.add(filename, text, line_num)

# Resources
@mcp.resource(
    name='resource_get_todos_for_file',
    description='Get all #TODOs in an array of strings for a given source file. Return empty array if no #TODOs found.',
    uri='todo://{filename}/todos',
    )
def get_todos_for_file(
        filename: Annotated[str, 'The name of the file to get #TODOs for']
        ) -> list[str]:
    todos = Todo_db.get(filename)
    return [text for text in todos.values()]

# Start the MCP server
def main():
    mcp.run()

if __name__ == "__main__":
    main()