package com.revolut.helloworld;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Optional;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class HelloWorldControllerTest {

	@Mock
	private UserRepository userRepository;

	@InjectMocks
	private HelloWorldApplication helloWorldController;

	private MockMvc mockMvc;

	@Test
	public void testGetUser_BirthdayInNDays() throws Exception {
		String username = "John";
		LocalDate dob = LocalDate.now().plusDays(5);

		User user = new User();
		user.setUsername(username);
		user.setDateOfBirth(dob);

		when(userRepository.findByUsername(eq(username))).thenReturn(Optional.of(user));

		mockMvc = MockMvcBuilders.standaloneSetup(helloWorldController).build();

		mockMvc.perform(MockMvcRequestBuilders.get("/hello/{username}", username)
						.accept(MediaType.APPLICATION_JSON))
				.andExpect(MockMvcResultMatchers.status().isOk())
				.andExpect(MockMvcResultMatchers.content().json("{\"message\":\"Hello, John! Your birthday is in 5 day(s).\"}"));
	}

	@Test
	public void testGetUser_BirthdayToday() throws Exception {
		String username = "Jane";
		LocalDate dob = LocalDate.now();

		User user = new User();
		user.setUsername(username);
		user.setDateOfBirth(dob);

		when(userRepository.findByUsername(eq(username))).thenReturn(Optional.of(user));

		mockMvc = MockMvcBuilders.standaloneSetup(helloWorldController).build();

		mockMvc.perform(MockMvcRequestBuilders.get("/hello/{username}", username)
						.accept(MediaType.APPLICATION_JSON))
				.andExpect(MockMvcResultMatchers.status().isOk())
				.andExpect(MockMvcResultMatchers.content().json("{\"message\":\"Hello, Jane! Happy birthday!\"}"));
	}

	@Test
	public void testGetUser_UserNotFound() throws Exception {
		String username = "NonExistentUser";

		when(userRepository.findByUsername(eq(username))).thenReturn(Optional.empty());

		mockMvc = MockMvcBuilders.standaloneSetup(helloWorldController).build();

		mockMvc.perform(MockMvcRequestBuilders.get("/hello/{username}", username)
						.accept(MediaType.APPLICATION_JSON))
				.andExpect(MockMvcResultMatchers.status().isNotFound());
	}

	@Test
	public void testSaveUser() throws Exception {
		String username = "John";
		LocalDate dob = LocalDate.now().plusDays(5);

		RequestDto requestDto = new RequestDto();
		requestDto.setDateOfBirth(dob);

		mockMvc = MockMvcBuilders.standaloneSetup(helloWorldController).build();

		mockMvc.perform(MockMvcRequestBuilders.put("/hello/{username}", username)
						.contentType(MediaType.APPLICATION_JSON)
						.content("{\"dateOfBirth\":\"" + dob.format(DateTimeFormatter.ISO_LOCAL_DATE) + "\"}"))
				.andExpect(MockMvcResultMatchers.status().isNoContent());
	}
}
