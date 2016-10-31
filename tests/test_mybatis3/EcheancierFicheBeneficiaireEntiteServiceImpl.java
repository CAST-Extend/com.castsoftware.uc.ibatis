package com.mycompany.comptenominatif;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

/**
 * @author myAuthor
 * Sample MyBatis3
 * 
 */
/**
 * Contrat du service EcheancierFicheBeneficiaireEntiteServiceImpl.
 */
@Component
@Transactional(propagation = Propagation.REQUIRED)
public class EcheancierFicheBeneficiaireEntiteServiceImpl extends
        AbstractGenericServiceEntite<EcheancierFicheBeneficiaire, EcheancierFicheBeneficiaireDTO> implements
        EcheancierFicheBeneficiaireEntiteService {

    /**
     * Mapper EcheancierFicheBeneficiaireEntityMapper.
     */
    @Autowired
    private EcheancierFicheBeneficiaireEntityMapper mapper;

    //Start of user code custom ProduitEntiteService service members

    //End of user code

    //Start of user code custom ProduitEntiteService service methods
    @Override
    public List<EcheancierFicheBeneficiaireDTO> selectEcheanciersADesactiver(final String pDateDuJour,
            final String codeEtablissement) {
        final List<EcheancierFicheBeneficiaireDTO> res = new ArrayList<EcheancierFicheBeneficiaireDTO>();

        final List<EcheancierFicheBeneficiaire> listeEcheanciers = mapper.selectEcheanciersADesactiver(pDateDuJour,
                codeEtablissement, LNStatutEchFicheBenefDTO.DESACTIVE);
        for (final EcheancierFicheBeneficiaire e : listeEcheanciers) {
            res.add(convert(e, EcheancierFicheBeneficiaireDTO.class));
        }

        return res;
    }

    @Override
    public List<EcheancierFicheBeneficiaireDTO> selectEcheanciersAActiver(final String pDateDuJour,
            final String codeEtablissement) {
        final List<EcheancierFicheBeneficiaireDTO> res = new ArrayList<EcheancierFicheBeneficiaireDTO>();

        final List<EcheancierFicheBeneficiaire> listeEcheanciers = mapper.selectEcheanciersAActiver(pDateDuJour,
                codeEtablissement, LNStatutEchFicheBenefDTO.ACTIVE);
        for (final EcheancierFicheBeneficiaire e : listeEcheanciers) {
            res.add(convert(e, EcheancierFicheBeneficiaireDTO.class));
        }

        return res;
    }

    //End of user code

    @Override
    public GenericMapper<EcheancierFicheBeneficiaire> getMapper() {
        return mapper;
    }

}
