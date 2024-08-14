from pydantic_settings import BaseSettings

# class BaseSchema(BaseModel):
#     model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

#     def __getitem__(self, item):
#         return getattr(self, item)

#     def __contains__(self, item):
#         try:
#             self.__getitem__(item)
#             return True
#         except AttributeError:
#             return False


class LambdaEnv(BaseSettings):
    feedback_form_url: str
