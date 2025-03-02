import React from 'react';

const ManualSync = () => {
    const handleSync = () => {
        fetch('http://localhost:8000/api/manual-sync/', {
            method: 'GET',
        })
        .then(response => {
            if (response.ok) {
                alert('Manual sync triggered successfully.');
            } else {
                alert('Failed to trigger manual sync.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while triggering manual sync.');
        });
    };

    return (
        <div>
            <button onClick={handleSync} className="btn btn-primary mt-3">Manual Sync</button>
        </div>
    );
};

export default ManualSync;