
import requests
from pathlib import Path
from ruamel.yaml import YAML
from pyloggerhelper import log


def update_nodes(config_path: Path, clash_url: str) -> None:
    log.info("task start", task_name="update_nodes")
    # yaml=YAML(typ='safe')
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    if not config_path.is_file():
        log.error("task target path not file", task_name="update_nodes")
        return

    with open(config_path, "r") as f:
        config = yaml.load(f)
    if config is None:
        config = {}
    if not config.get("mixed-port"):
        config["mixed-port"] = 7890
    if not config.get("redir-port"):
        config["redir-port"] = 7892
    if config.get("allow-lan") is None:
        config["allow-lan"] = True
    if not config.get("mode"):
        config["mode"] = "Rule"
    if not config.get("log-level"):
        config["log-level"] = "silent"
    if not config.get("external-controller"):
        config["external-controller"] = "0.0.0.0:9090"
    if config.get("secret") is None:
        config["secret"] = ""

    try:
        res = requests.get(clash_url)
        if res.status_code != 200:
            log.error("task query url get wrong http code", task_name="update_nodes", url=clash_url, status_code=res.status_code)
            return
        else:
            result = yaml.load(res.content)
            log.debug("task query url get config", task_name="update_nodes", url=clash_url, result=result)
            proxies = result["proxies"]
            dns = result["dns"]
            config["dns"] = dns
            config["proxies"] = proxies
            with open(config_path, "w") as wf:
                yaml.dump(config, wf)
    except Exception as e:
        log.error(
            "task query get unexpected error",
            task_name="update_nodes",
            error_type=str(type(e)),
            error_message=str(e),
            exc_info=True,
            stack_info=True
        )
        return
