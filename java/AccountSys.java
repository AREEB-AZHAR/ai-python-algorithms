import java.util.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * AccountSys - Complex Computing Problem (CCP) Implementation
 * * This system manages bank accounts, transactions, and enforces business rules
 * such as overdraft limits.
 */
public class AccountSys {

    // --- Inner Classes for Data Structures ---

    static class Transaction {
        private String type; // "Deposit" or "Withdrawal"
        private double amount;
        private LocalDateTime timestamp;

        public Transaction(String type, double amount) {
            this.type = type;
            this.amount = amount;
            this.timestamp = LocalDateTime.now();
        }

        @Override
        public String toString() {
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
            return String.format("[%s] %s: $%.2f", timestamp.format(formatter), type, amount);
        }
    }

    static class Account {
        private String accNum;
        private String details; // Personal details
        private double balance;
        private double overdraftLimit;
        private List<Transaction> transactionHistory;

        public Account(String accNum, String details, double overdraftLimit) {
            this.accNum = accNum;
            this.details = details;
            this.overdraftLimit = overdraftLimit;
            this.balance = 0.0;
            this.transactionHistory = new ArrayList<>();
        }

        public String getAccNum() { return accNum; }
        public String getDetails() { return details; }
        public double getBalance() { return balance; }
        public double getOverdraftLimit() { return overdraftLimit; }
        public List<Transaction> getTransactionHistory() { return transactionHistory; }

        public void setDetails(String details) { this.details = details; }
        public void setOverdraftLimit(double limit) { this.overdraftLimit = limit; }

        // Core logic: Enforce (Balance + Limit >= 0)
        public boolean canWithdraw(double amount) {
            return (balance - amount) + overdraftLimit >= 0;
        }

        public void deposit(double amount) {
            if (amount <= 0) throw new IllegalArgumentException("Deposit amount must be positive.");
            this.balance += amount;
            this.transactionHistory.add(new Transaction("Deposit", amount));
        }

        public void withdraw(double amount) {
            if (amount <= 0) throw new IllegalArgumentException("Withdrawal amount must be positive.");
            if (!canWithdraw(amount)) {
                throw new IllegalStateException("Transaction declined: Exceeds overdraft limit.");
            }
            this.balance -= amount;
            this.transactionHistory.add(new Transaction("Withdrawal", amount));
        }
    }

    // --- Main System Logic ---

    private Map<String, Account> accounts;
    private Scanner scanner;

    public AccountSys() {
        this.accounts = new HashMap<>();
        this.scanner = new Scanner(System.in);
    }

    public void start() {
        boolean running = true;
        while (running) {
            printMenu();
            String choice = scanner.nextLine();
            try {
                switch (choice) {
                    case "1": createAccount(); break;
                    case "2": deleteAccount(); break;
                    case "3": performDeposit(); break;
                    case "4": performWithdrawal(); break;
                    case "5": modifyPersonalDetails(); break;
                    case "6": adjustOverdraftLimit(); break;
                    case "7": generateStatement(); break;
                    case "8": displayBalance(); break;
                    case "9": displayDetails(); break;
                    case "0": running = false; break;
                    default: System.out.println("Invalid option. Please try again.");
                }
            } catch (Exception e) {
                System.out.println("Error: " + e.getMessage());
            }
            System.out.println();
        }
        System.out.println("System terminated.");
    }

    private void printMenu() {
        System.out.println("=== AccountSys Management ===");
        System.out.println("1. Create New Account");
        System.out.println("2. Delete Account");
        System.out.println("3. Deposit");
        System.out.println("4. Withdraw");
        System.out.println("5. Modify Personal Info");
        System.out.println("6. Adjust Overdraft Limit");
        System.out.println("7. Generate Statement");
        System.out.println("8. Display Balance");
        System.out.println("9. Display Personal Details");
        System.out.println("0. Exit");
        System.out.print("Select an option: ");
    }

    // --- Operations ---

    private void createAccount() {
        System.out.print("Enter New Account Number: ");
        String accNum = scanner.nextLine();
        if (accounts.containsKey(accNum)) {
            throw new IllegalArgumentException("Account number already exists.");
        }
        System.out.print("Enter Customer Details (Name/Address): ");
        String details = scanner.nextLine();
        System.out.print("Enter Overdraft Limit: ");
        double limit = Double.parseDouble(scanner.nextLine());

        accounts.put(accNum, new Account(accNum, details, limit));
        System.out.println("Account created successfully.");
    }

    private void deleteAccount() {
        System.out.print("Enter Account Number to Delete: ");
        String accNum = scanner.nextLine();
        if (!accounts.containsKey(accNum)) {
            throw new IllegalArgumentException("Account not found.");
        }
        accounts.remove(accNum);
        System.out.println("Account deleted successfully.");
    }

    private void performDeposit() {
        Account acc = getAccountOrThrow();
        System.out.print("Enter Deposit Amount: ");
        double amount = Double.parseDouble(scanner.nextLine());
        acc.deposit(amount);
        System.out.println("Deposit successful. New Balance: " + acc.getBalance());
    }

    private void performWithdrawal() {
        Account acc = getAccountOrThrow();
        System.out.print("Enter Withdrawal Amount: ");
        double amount = Double.parseDouble(scanner.nextLine());
        acc.withdraw(amount); // Validation happens inside Account class
        System.out.println("Withdrawal successful. New Balance: " + acc.getBalance());
    }

    private void modifyPersonalDetails() {
        Account acc = getAccountOrThrow();
        System.out.print("Enter New Personal Details: ");
        String details = scanner.nextLine();
        acc.setDetails(details);
        System.out.println("Details updated.");
    }

    private void adjustOverdraftLimit() {
        Account acc = getAccountOrThrow();
        System.out.print("Enter New Overdraft Limit: ");
        double limit = Double.parseDouble(scanner.nextLine());
        
        // Check if current balance violates new limit immediately
        if ((acc.getBalance() + limit) < 0) {
            throw new IllegalStateException("Cannot lower limit: Current negative balance exceeds new limit.");
        }
        
        acc.setOverdraftLimit(limit);
        System.out.println("Overdraft limit updated.");
    }

    private void generateStatement() {
        Account acc = getAccountOrThrow();
        System.out.println("--- Transaction Statement for " + acc.getAccNum() + " ---");
        for (Transaction t : acc.getTransactionHistory()) {
            System.out.println(t);
        }
        System.out.println("-------------------------------------------");
    }

    private void displayBalance() {
        Account acc = getAccountOrThrow();
        System.out.println("Current Balance: $" + acc.getBalance());
        System.out.println("Overdraft Limit: $" + acc.getOverdraftLimit());
        System.out.println("Available Funds: $" + (acc.getBalance() + acc.getOverdraftLimit()));
    }

    private void displayDetails() {
        Account acc = getAccountOrThrow();
        System.out.println("Account Number: " + acc.getAccNum());
        System.out.println("Customer Details: " + acc.getDetails());
    }

    private Account getAccountOrThrow() {
        System.out.print("Enter Account Number: ");
        String accNum = scanner.nextLine();
        if (!accounts.containsKey(accNum)) {
            throw new IllegalArgumentException("Account not found.");
        }
        return accounts.get(accNum);
    }

    public static void main(String[] args) {
        AccountSys sys = new AccountSys();
        sys.start();
    }
}