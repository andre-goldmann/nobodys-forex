package jdg.digital.forexbackend.domain.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name= "\"Trades\"")
public class SignalEntity {

    @Id
    private Integer id;

    private String symbol;

    private String strategy;

    private String type;

    private Double entry;

    private Double sl;

    private Double tp;

    private Double lots;

    private String stamp;

    public SignalEntity() {
    }

    public Integer getId() {
        return id;
    }


    public Double getEntry() {
        return entry;
    }

    public void setEntry(Double entry) {
        this.entry = entry;
    }

    public Double getSl() {
        return sl;
    }

    public void setSl(Double sl) {
        this.sl = sl;
    }

    public Double getTp() {
        return tp;
    }

    public void setTp(Double tp) {
        this.tp = tp;
    }


    public void setId(Integer id) {
        this.id = id;
    }

    public String getSymbol() {
        return symbol;
    }

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

    public String getStrategy() {
        return strategy;
    }

    public void setStrategy(String strategy) {
        this.strategy = strategy;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getStamp() {
        return stamp;
    }

    public void setStamp(String stamp) {
        this.stamp = stamp;
    }

    public Double getLots() {
        return lots;
    }

    public void setLots(Double lots) {
        this.lots = lots;
    }

    @Override
    public String toString() {
        return "TradesEntity{" +
                "id=" + id +
                ", symbol='" + symbol + '\'' +
                ", strategy='" + strategy + '\'' +
                ", type='" + type + '\'' +
                ", entry=" + entry +
                ", sl=" + sl +
                ", tp=" + tp +
                '}';
    }
}
