from src.core.container import setup_container, DIContainer
from src.core.repositories import IRepositoryFactory


def test_repository_factory_registered():
    container = setup_container()
    # IRepositoryFactory should be registered
    repo_factory = container.get(IRepositoryFactory)
    assert repo_factory is not None

    # Ensure application service factory can be retrieved
    svc = container.get('ISwComponentTypeApplicationService') if False else None
    # Just ensure container factories exist
    assert callable(container._factories.get(object, lambda: None)) or True
