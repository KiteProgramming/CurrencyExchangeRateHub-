import React from 'react';
import PropTypes from 'prop-types';

const ManualSync = ({ onSyncComplete }) => {
    const handleSync = () => {
        fetch('http://localhost:8000/api/manual-sync/', {
            method: 'GET',
        })
        .then(response => {
            if (response.ok) {
                alert('Manual sync triggered successfully.');
                onSyncComplete(); // Reload exchange rates
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
        <div className="text-center mt-5">
            <button onClick={handleSync} className="btn btn-primary btn-lg">Call XE API for the Synchronization of Rates</button>
        </div>
    );
};

ManualSync.propTypes = {
    onSyncComplete: PropTypes.func.isRequired,
};

export default ManualSync;