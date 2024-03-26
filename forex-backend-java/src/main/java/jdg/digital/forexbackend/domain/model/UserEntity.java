package jdg.digital.forexbackend.model;

import jakarta.persistence.*;
import org.hibernate.annotations.GenericGenerator;
import org.springframework.data.domain.Persistable;

import java.util.UUID;

@Entity
@Table(name= "users")
// DO not use Lombock her
public class UserEntity implements Persistable<UUID>  {

    @Id
    @GeneratedValue(generator = "uuid")
    @GenericGenerator(name = "uuid", strategy = "uuid2")
    UUID id;

    @Column(name = "fullname")
    String fullName;
    //Integer age;
    @Column(name = "email")
    String email;
    //String password;
    //posts: Post[];
    //OffsetDateTime createdAt;
    //OffsetDateTime updatedAt;
    //OffsetDateTime deletedAt;

    @Override
    public UUID getId() {
        return id;
    }

    @Override
    public boolean isNew() {
        return id == null;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }
}
