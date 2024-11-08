module com.group13.coffeemanagement {
    requires javafx.controls;
    requires javafx.fxml;

    requires transitive com.google.gson;
    requires transitive javafx.graphics;
    requires javafx.base;

    opens com.group13.coffeemanagement.enums to com.google.gson;
    opens com.group13.coffeemanagement.model to com.google.gson, javafx.base;
    opens com.group13.coffeemanagement.database to com.google.gson;
    opens com.group13.coffeemanagement to com.google.gson;
    opens com.group13.coffeemanagement.controller to javafx.fxml;

    exports com.group13.coffeemanagement;
}