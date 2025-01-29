from nautobot.apps.jobs import Job, register_jobs


class HelloWorld(Job):

    class Meta:
        name = "Hello World 60!"
        description = "Simple job that showcases importing from a git repository."
        has_sensitive_variables = False
        read_only = True

    def run(self):
        self.logger.info("Hello World 60!")


register_jobs(HelloWorld)
