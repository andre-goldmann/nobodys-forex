package jdg.digital.bookstore.domain;

import jdg.digital.bookstore.domain.model.Book;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BookRepository extends JpaRepository<Book, Long> {
}
