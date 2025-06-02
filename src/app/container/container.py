import aioinject

from app import infrastructure, service_layer
from app.configs import Settings

from .wrappers import PostgresDatabaseWrapper

container = aioinject.Container()

# settings
container.register(aioinject.Object(Settings()))

# infrastructure
container.register(
    aioinject.Singleton(PostgresDatabaseWrapper, infrastructure.APostgresDatabase),
    aioinject.Singleton(infrastructure.SchedulerManager, infrastructure.ASchedulerManager),
)

# service layer
container.register(
    aioinject.Transient(service_layer.UnitOfWork, service_layer.AUnitOfWork),
    aioinject.Transient(service_layer.ConversationsService, service_layer.AConversationsService),
)
