"""
AUTHOR: EDDY FAKHRY
DATE:   15/10/2016
"""
from app import create_app
import pytest


@pytest.fixture
def app():
    app = create_app()
    return app

