// Initialize charts
let sentimentChart = null;
let trendingChart = null;

// Fetch and update data every 30 seconds
setInterval(updateData, 30000);

// Initial data load
updateData();

async function updateData() {
    try {
        // Fetch tweets
        const tweetsResponse = await fetch('/api/tweets');
        const tweets = await tweetsResponse.json();
        updateTweetsList(tweets);
        updateSentimentChart(tweets);

        // Fetch trending topics
        const trendingResponse = await fetch('/api/trending');
        const trending = await trendingResponse.json();
        updateTrendingChart(trending);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateTweetsList(tweets) {
    const tweetsList = document.getElementById('tweetsList');
    tweetsList.innerHTML = tweets.map(tweet => `
        <div class="list-group-item">
            <div class="tweet-text">${tweet.text}</div>
            <div class="tweet-meta">
                <span class="sentiment-${getSentimentClass(tweet.sentiment)}">
                    Sentiment: ${tweet.sentiment.toFixed(2)}
                </span>
                <span class="ms-3">${new Date(tweet.created_at).toLocaleString()}</span>
            </div>
        </div>
    `).join('');
}

function updateSentimentChart(tweets) {
    const sentimentData = {
        positive: 0,
        neutral: 0,
        negative: 0
    };

    tweets.forEach(tweet => {
        if (tweet.sentiment > 0.1) sentimentData.positive++;
        else if (tweet.sentiment < -0.1) sentimentData.negative++;
        else sentimentData.neutral++;
    });

    if (sentimentChart) {
        sentimentChart.destroy();
    }

    const ctx = document.getElementById('sentimentChart').getContext('2d');
    sentimentChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [{
                data: [sentimentData.positive, sentimentData.neutral, sentimentData.negative],
                backgroundColor: ['#28a745', '#6c757d', '#dc3545']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function updateTrendingChart(trending) {
    if (trendingChart) {
        trendingChart.destroy();
    }

    const ctx = document.getElementById('trendingChart').getContext('2d');
    trendingChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: trending.map(item => item[0]),
            datasets: [{
                label: 'Mentions',
                data: trending.map(item => item[1]),
                backgroundColor: '#007bff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function getSentimentClass(sentiment) {
    if (sentiment > 0.1) return 'positive';
    if (sentiment < -0.1) return 'negative';
    return 'neutral';
} 