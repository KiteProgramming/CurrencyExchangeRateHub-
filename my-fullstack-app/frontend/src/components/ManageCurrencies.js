import React, { useState, useEffect } from 'react';
import CurrencyExchange from './CurrencyExchange';
import ManualSync from './ManualSync';

const ManageCurrencies = () => {
    const [currencies, setCurrencies] = useState([]);
    const [exchangeRates, setExchangeRates] = useState([]);
    const [code, setCode] = useState('');
    const [name, setName] = useState('');

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
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>Code</th>
                        <th>Name</th>
                    </tr>
                </thead>
                <tbody>
                    {currencies.map((currency, index) => (
                        <tr key={index}>
                            <td>{currency.code}</td>
                            <td>{currency.name}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <CurrencyExchange onRateAdded={reloadExchangeRates} />
            <h2 className="my-4">Exchange Rates</h2>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>Pair</th>
                        <th>Rate</th>
                        <th>Last Updated</th>
                    </tr>
                </thead>
                <tbody>
                    {exchangeRates.map((rate, index) => (
                        <tr key={index}>
                            <td>{rate.pair}</td>
                            <td>{rate.rate}</td>
                            <td>{new Date(rate.updated_at).toLocaleString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <ManualSync onSyncComplete={reloadExchangeRates} />
        </div>
    );
};

export default ManageCurrencies;