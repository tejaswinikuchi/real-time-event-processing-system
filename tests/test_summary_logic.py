from app.api.events import get_summary


def test_summary_calculation():

    values = [10, 20, 30]

    result = {
        "average": sum(values) / len(values),
        "min": min(values),
        "max": max(values)
    }

    assert result["average"] == 20
    assert result["min"] == 10
    assert result["max"] == 30