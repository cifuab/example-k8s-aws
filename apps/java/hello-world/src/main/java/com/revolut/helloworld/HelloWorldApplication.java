package com.revolut.helloworld;

import jakarta.persistence.*;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.annotation.Id;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.Optional;

@SpringBootApplication
public class HelloWorldApplication {

	public static void main(String[] args) {
		SpringApplication.run(HelloWorldApplication.class, args);
	}
}

@Entity
class User {
	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}

	public LocalDate getDateOfBirth() {
		return dateOfBirth;
	}

	public void setDateOfBirth(LocalDate dateOfBirth) {
		this.dateOfBirth = dateOfBirth;
	}

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@Column(unique = true)
	private String username;

	private LocalDate dateOfBirth;

	public User(Long id, String username, LocalDate dateOfBirth) {
		this.id = id;
		this.username = username;
		this.dateOfBirth = dateOfBirth;
	}

	// Constructors, getters, setters, and other methods

	// Ensure the date of birth is always before today
	@PrePersist
	@PreUpdate
	private void validateDateOfBirth() {
		if (dateOfBirth != null && dateOfBirth.isAfter(LocalDate.now())) {
			throw new IllegalArgumentException("Invalid date of birth. It must be before today.");
		}
	}
}

@Repository
interface UserRepository extends JpaRepository<User, Long> {
	Optional<User> findByUsername(String username);
}
