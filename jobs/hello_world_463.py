from nautobot.apps.jobs import Job, register_jobs


class HelloWorld(Job):

    class Meta:
        name = "Hello World 463!"
        description = "Simple job that showcases importing from a git repository."
        has_sensitive_variables = False
        read_only = True

    def run(self):
        self.logger.info("Hello World 463!")


register_jobs(HelloWorld)
