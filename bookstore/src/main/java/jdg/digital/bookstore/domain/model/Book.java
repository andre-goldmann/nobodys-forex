package jdg.digital.bookstore.domain.model;
import jakarta.persistence.*;


@Entity
@Table(name = "books")
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String listName;
    private String displayName;
    private String bestsellersDate;
    private String publishedDate;
    private int rank;
    private int rankLastWeek;
    private int weeksOnList;
    private int asterisk;
    private int dagger;
    private String amazonProductUrl;
    private String title;
    private String description;
    private String contributor;
    private String author;
    private String contributorNote;
    private double price;
    private String ageGroup;
    private String publisher;
    private String primaryIsbn13;
    private Long primaryIsbn10;

    // Getters and setters
}
