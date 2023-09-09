import os.path

from fastapi import APIRouter

creator = APIRouter()


@creator.post('/create_recorder')
async def create_new_recorder(
        recorder_name: str,
        recorder_types: str,
):
    with open('template_route.txt', 'r') as f:
        lines = f.readlines()

    replacements = {'${{route_name}}': recorder_name,
                    '${{create_record_args}}': recorder_types,
                    '${{get_record_args}}': "id: int"}

    new_lines = []
    for line in lines:
        new_line = line
        for k, v in replacements.items():
            new_line = new_line.replace(k, v)
        new_lines.append(new_line)

    with open(os.path.join('routes', recorder_name + '.py'), 'w+') as f:
        f.writelines(new_lines)
