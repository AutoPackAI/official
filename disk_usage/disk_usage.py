import psutil
from autopack import Pack
from pydantic import BaseModel


class DiskUsageArgsSchema(BaseModel):
    pass


class DiskUsage(Pack):
    name = "disk_usage"
    description = "Get the current OS name and version information."
    dependencies = ["psutil"]
    args_schema = DiskUsageArgsSchema
    categories = ["System Info"]

    def _run(self):
        # Currently we will only support root directory
        usage = psutil.disk_usage("/")
        used = round(usage.used / 1024 / 1024 / 1024, 2)
        total = round(usage.total / 1024 / 1024 / 1024, 2)
        free = round(usage.free / 1024 / 1024 / 1024, 2)

        return f"""Total: {total} GB. Used: {used} GB. Available: {free} GB". Percent Used: {usage.percent * 100}%"""

    async def _arun(self):
        return self.run()
