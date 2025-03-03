import React, { useState, useEffect } from 'react';
import CurrencyExchange from './CurrencyExchange';
import ManualSync from './ManualSync';

const getCsrfToken = () => {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return '';
};

const ManageCurrencies = () => {
    const [currencies, setCurrencies] = useState([]);
    const [exchangeRates, setExchangeRates] = useState([]);
    const [code, setCode] = useState('');
    const [name, setName] = useState('');
    const [searchTerm, setSearchTerm] = useState('');
    const [editingCurrency, setEditingCurrency] = useState(null);
    const [newCurrencyCode, setNewCurrencyCode] = useState('');
    const [newCurrencyName, setNewCurrencyName] = useState('');
    const [editingRate, setEditingRate] = useState(null);
    const [newRate, setNewRate] = useState('');

    useEffect(() => {
        fetch('http://localhost:8000/api/currencies/')
            .then(response => response.json())
            .then(data => setCurrencies(data));

        fetch('http://localhost:8000/api/exchange-rates/')
            .then(response => response.json())
            .then(data => setExchangeRates(data));
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        fetch('http://localhost:8000/api/currencies/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code, name, interval_minutes: 60 }),
        })
            .then(response => response.json())
            .then(data => {
                setCurrencies([...currencies, data]);
                setCode('');
                setName('');
            });
    };

    const reloadExchangeRates = () => {
        console.log('Reloading exchange rates');
        fetch('http://localhost:8000/api/exchange-rates/')
            .then(response => response.json())
            .then(data => setExchangeRates(data));
    };

    const handleEditCurrency = (currency) => {
        setEditingCurrency(currency);
        setNewCurrencyCode(currency.code);
        setNewCurrencyName(currency.name);
    };

    const handleDeleteCurrency = (code) => {
        const csrfToken = getCsrfToken();
        fetch(`http://localhost:8000/api/delete-currency/${code}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
            .then(response => {
                if (response.ok) {
                    setCurrencies(currencies.filter(currency => currency.code !== code));
                } else {
                    alert('Failed to delete currency.');
                }
            });
    };

    const handleUpdateCurrency = (e) => {
        e.preventDefault();
        const csrfToken = getCsrfToken();
        fetch(`http://localhost:8000/api/update-currency/${editingCurrency.code}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ code: newCurrencyCode, name: newCurrencyName }),
        })
            .then(response => {
                if (response.ok) {
                    setEditingCurrency(null);
                    setNewCurrencyCode('');
                    setNewCurrencyName('');
                    fetch('http://localhost:8000/api/currencies/')
                        .then(response => response.json())
                        .then(data => setCurrencies(data));
                } else {
                    alert('Failed to update currency.');
                }
            });
    };

    const handleEditRate = (rate) => {
        setEditingRate(rate);
        setNewRate(rate.rate);
    };

    const handleDeleteRate = (pair) => {
        const csrfToken = getCsrfToken();
        fetch(`http://localhost:8000/api/delete-exchange-rate/${pair}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
            .then(response => {
                if (response.ok) {
                    reloadExchangeRates();
                } else {
                    alert('Failed to delete exchange rate.');
                }
            });
    };

    const handleUpdateRate = (e) => {
        e.preventDefault();
        const csrfToken = getCsrfToken();
        fetch(`http://localhost:8000/api/update-exchange-rate/${editingRate.pair}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ rate: newRate }),
        })
            .then(response => {
                if (response.ok) {
                    setEditingRate(null);
                    setNewRate('');
                    reloadExchangeRates();
                } else {
                    alert('Failed to update exchange rate.');
                }
            });
    };

    const filteredCurrencies = currencies.filter(currency =>
        currency.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
        currency.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const filteredRates = exchangeRates.filter(rate =>
        rate.pair.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="container">
            <h1 className="my-4">Manage Currencies</h1>
            <form onSubmit={handleSubmit} className="mb-4">
                <div className="form-group">
                    <input
                        type="text"
                        className="form-control"
                        placeholder="Currency Code"
                        value={code}
                        onChange={(e) => setCode(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <input
                        type="text"
                        className="form-control"
                        placeholder="Currency Name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">Add Currency</button>
            </form>
            <h2 className="my-4">Currencies</h2>
            <div className="d-flex justify-content-between align-items-center mb-2">                
                <input
                    type="text"
                    className="form-control w-25"
                    placeholder="Search by code or name"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>Code</th>
                        <th>Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredCurrencies.map((currency, index) => (
                        <tr key={index}>
                            <td>{currency.code}</td>
                            <td>
                                {editingCurrency && editingCurrency.code === currency.code ? (
                                    <form onSubmit={handleUpdateCurrency}>
                                        <input
                                            type="text"
                                            className="form-control"
                                            value={newCurrencyCode}
                                            onChange={(e) => setNewCurrencyCode(e.target.value)}
                                            required
                                        />
                                        <input
                                            type="text"
                                            className="form-control"
                                            value={newCurrencyName}
                                            onChange={(e) => setNewCurrencyName(e.target.value)}
                                            required
                                        />
                                        <button type="submit" className="btn btn-primary btn-sm">Save</button>
                                        <button type="button" className="btn btn-secondary btn-sm" onClick={() => setEditingCurrency(null)}>Cancel</button>
                                    </form>
                                ) : (
                                    currency.name
                                )}
                            </td>
                            <td>
                                <button className="btn btn-warning btn-sm" onClick={() => handleEditCurrency(currency)}>
                                    <i className="fas fa-pencil-alt"></i>
                                </button>
                                <button className="btn btn-danger btn-sm" onClick={() => handleDeleteCurrency(currency.code)}>
                                    <i className="fas fa-trash-alt"></i>
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <CurrencyExchange onRateAdded={reloadExchangeRates} />
            <h2 className="my-4">Exchange Rates</h2>
            <div className="d-flex justify-content-between align-items-center mb-2">                
                <input
                    type="text"
                    className="form-control w-25"
                    placeholder="Search by pair"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>Pair</th>
                        <th>Rate</th>
                        <th>Last Updated</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredRates.map((rate, index) => (
                        <tr key={index}>
                            <td>{rate.pair}</td>
                            <td>
                                {editingRate && editingRate.pair === rate.pair ? (
                                    <form onSubmit={handleUpdateRate}>
                                        <input
                                            type="text"
                                            className="form-control"
                                            value={newRate}
                                            onChange={(e) => setNewRate(e.target.value)}
                                            required
                                        />
                                        <button type="submit" className="btn btn-primary btn-sm">Save</button>
                                        <button type="button" className="btn btn-secondary btn-sm" onClick={() => setEditingRate(null)}>Cancel</button>
                                    </form>
                                ) : (
                                    rate.rate
                                )}
                            </td>
                            <td>{new Date(rate.updated_at).toLocaleString()}</td>
                            <td>
                                <button className="btn btn-warning btn-sm" onClick={() => handleEditRate(rate)}>
                                    <i className="fas fa-pencil-alt"></i>
                                </button>
                                <button className="btn btn-danger btn-sm" onClick={() => handleDeleteRate(rate.pair)}>
                                    <i className="fas fa-trash-alt"></i>
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <ManualSync onSyncComplete={reloadExchangeRates} />
        </div>
    );
};

export default ManageCurrencies;