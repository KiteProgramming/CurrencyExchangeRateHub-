import React, { useState, useEffect } from 'react';

const ManageCurrencies = () => {
    const [currencies, setCurrencies] = useState([]);
    const [code, setCode] = useState('');
    const [name, setName] = useState('');
    const [interval, setInterval] = useState(60);

    useEffect(() => {
        fetch('http://localhost:8000/api/currencies/')
            .then(response => response.json())
            .then(data => setCurrencies(data));
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        fetch('http://localhost:8000/api/currencies/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code, name, interval_minutes: interval }),
        })
            .then(response => response.json())
            .then(data => {
                setCurrencies([...currencies, data]);
                setCode('');
                setName('');
                setInterval(60);
            });
    };

    return (
        <div>
            <h1>Manage Currencies</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Currency Code"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Currency Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <input
                    type="number"
                    placeholder="Interval (minutes)"
                    value={interval}
                    onChange={(e) => setInterval(e.target.value)}
                />
                <button type="submit">Add Currency</button>
            </form>
            <ul>
                {currencies.map((currency, index) => (
                    <li key={index}>{currency.code}: {currency.name} (Interval: {currency.interval_minutes} minutes)</li>
                ))}
            </ul>
        </div>
    );
};

export default ManageCurrencies;