package com.mycompany.comptenominatif.mapper;

import java.util.List;

import org.apache.ibatis.annotations.Param;

/**
 * Contrat du mapper EcheancierFicheBeneficiaireEntityMapper.
 */
public interface EcheancierFicheBeneficiaireEntityMapper extends GenericMapper<EcheancierFicheBeneficiaire> {

    //Start of user code custom methods
    String P_DATE_ACTUELLE = "pDateActuelle";

    /**
     * Permet de recuperer les EcheancierFicheBeneficiaire inférieures à pDateActuelle
     * 
     * @param pDateActuelle
     * @param codeEtablissement
     * @param desactive
     * @return la List<EcheancierFicheBeneficiaire>
     */
    List<EcheancierFicheBeneficiaire> selectEcheanciersADesactiver(@Param(P_DATE_ACTUELLE) String pDateActuelle,
            @Param("codeEtablissement") String codeEtablissement, @Param("pDesactive") String desactive);

    /**
     * @param pDateActuelle
     * @param codeEtablissement
     * @param active
     * @return
     */
    List<EcheancierFicheBeneficiaire> selectEcheanciersAActiver(@Param(P_DATE_ACTUELLE) String pDateActuelle,
            @Param("codeEtablissement") String codeEtablissement, @Param("pActive") String active);

    //End of user code
}
