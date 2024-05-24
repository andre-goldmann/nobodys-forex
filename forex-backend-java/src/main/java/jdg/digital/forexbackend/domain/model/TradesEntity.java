package jdg.digital.forexbackend.domain.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name= "\"Trades\"")
public class TradesEntity {

    @Id
    private Integer id;

    private String symbol;

    private String strategy;

    private String type;

    private Double entry;

    private Double sl;

    private Double tp;

    private Double lots;

    private Double spread;

    //private Integer tradeid;
    private String activated;

    private Double openprice;

    private Double swap;

    private Double profit;

    private String closed;

    private Double commision;

    private Double exit;

    public TradesEntity() {
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

    public Double getLots() {
        return lots;
    }

    public void setLots(Double lots) {
        this.lots = lots;
    }

    public Double getSpread() {
        return spread;
    }

    public void setSpread(Double spread) {
        this.spread = spread;
    }

    public Double getOpenprice() {
        return openprice;
    }

    public void setOpenprice(Double openprice) {
        this.openprice = openprice;
    }

    public Double getSwap() {
        return swap;
    }

    public void setSwap(Double swap) {
        this.swap = swap;
    }

    public Double getProfit() {
        return profit;
    }

    public void setProfit(Double profit) {
        this.profit = profit;
    }

    public Double getCommision() {
        return commision;
    }

    public void setCommision(Double commision) {
        this.commision = commision;
    }

    public Double getExit() {
        return exit;
    }

    public void setExit(Double exit) {
        this.exit = exit;
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

    public String getActivated() {
        return activated;
    }

    public void setActivated(String activated) {
        this.activated = activated;
    }

    public String getClosed() {
        return closed;
    }

    public void setClosed(String closed) {
        this.closed = closed;
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
                ", lots=" + lots +
                ", spread=" + spread +
                ", activated='" + activated + '\'' +
                ", openprice=" + openprice +
                ", swap=" + swap +
                ", profit=" + profit +
                ", closed='" + closed + '\'' +
                ", commision=" + commision +
                ", exit=" + exit +
                '}';
    }
}
