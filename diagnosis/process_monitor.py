import psutil


WINDOWS_PROCESSES = {
    "memcompression",
    "system",
    "registry",
    "explorer.exe",
    "svchost.exe",
    "dwm.exe",
    "lsass.exe",
    "services.exe",
    "winlogon.exe",
    "csrss.exe",
    "smss.exe",
}


VIRTUALIZATION_PROCESSES = {
    "vmmem",
    "vmmemwsl",
    "vmmemwsl.exe",
}


def classify_process(name):
    name_lower = name.lower()

    if name_lower in WINDOWS_PROCESSES:
        return "Windows"

    if name_lower in VIRTUALIZATION_PROCESSES:
        return "WSL/仮想環境"

    return "アプリケーション"


def get_top_memory_processes(limit=10):
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "memory_info"]
    ):
        try:
            info = process.info
            memory_info = info["memory_info"]

            if memory_info is None:
                continue

            memory_mb = memory_info.rss / (1024 ** 2)

            name = info["name"] or "Unknown"

            processes.append(
                {
                    "pid": info["pid"],
                    "name": name,
                    "memory_mb": memory_mb,
                    "category": classify_process(name),
                }
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    processes.sort(
        key=lambda process: process["memory_mb"],
        reverse=True,
    )

    return processes[:limit]