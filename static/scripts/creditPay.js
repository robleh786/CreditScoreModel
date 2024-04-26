document.addEventListener('DOMContentLoaded', function() {
    let rangeInput = document.getElementById('your_payment');
    let amountDisplay = document.getElementById('payment-amount-display');
    let cardBalanceInput = document.getElementById('card_balance');
    
    // Update the display as the slider moves
    rangeInput.addEventListener('input', function() {
        amountDisplay.textContent = `£${this.value}`;
    });

    // Adjust the slider's max value and the displayed repayment amount
    // when the credit card balance input is changed
    cardBalanceInput.addEventListener('input', function() {
        const balance = parseFloat(this.value) || 0;
        const maxRepayment = Math.max(1000, balance / 10);
        rangeInput.max = maxRepayment;
        rangeInput.value = maxRepayment; // Set slider value to max by default
        amountDisplay.textContent = `£${rangeInput.value}`;
    });

    document.getElementById('calculate-button').addEventListener('click', initiateCreditCardPayoffCalculation);

    function initiateCreditCardPayoffCalculation() {
        const balance = parseFloat(cardBalanceInput.value);
        const interestRate = parseFloat(document.getElementById('interest_rate').value);
        const payment = parseFloat(rangeInput.value);

        if (isNaN(balance) || isNaN(interestRate) || isNaN(payment)) {
            alert("Please enter valid numbers for all fields.");
            return;
        }

        const result = calculateCreditCardPayoff(balance, interestRate, payment);
        updateUIWithResults(result);
    }

    function calculateCreditCardPayoff(balance, interestRate, monthlyPayment) {
        let totalInterest = 0;
        let months = 0;

        while (balance > 0) {
            let monthlyInterest = balance * (interestRate / 12 / 100);
            let principal = monthlyPayment - monthlyInterest;
            if (principal <= 0) {
                alert("Your monthly payment is too low to cover the interest. Please increase your payment amount.");
                break;
            }
            balance -= principal;
            totalInterest += monthlyInterest;
            months++;
        }

        return {
            totalInterest: totalInterest,
            payoffTime: months
        };
    }

    function updateUIWithResults(result) {
        document.getElementById('payment-amount').textContent = `Monthly Payment: £${parseFloat(rangeInput.value).toFixed(2)}`;
        document.getElementById('total-interest').textContent = `Total Interest Paid: £${result.totalInterest.toFixed(2)}`;
        document.getElementById('payback-time').textContent = `Payoff Time: ${getYearsMonths(result.payoffTime)}`;
    }

    function getYearsMonths(months){
        let years = Math.floor(months / 12);
        let remainderMonths = months % 12;
        return `${years} years and ${remainderMonths} months`;
    }
});
