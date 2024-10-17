from pydantic import BaseModel, AnyUrl, IPvAnyAddress


class AddressModel(BaseModel):
    """Some kind of address which is compatible with socket.gethostbyname"""

    address: AnyUrl | IPvAnyAddress


class RequestDataModel(BaseModel):
    """Input model for the request_data endpoint"""

    input_data: AddressModel
